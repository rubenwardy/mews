from app import app
from app.tasks import celery, TaskError
from app.tasks.sync import importAllMusic, getArtistsInfo, getAlbumsInfo
from flask_caching import Cache
from contextlib import contextmanager
from celery.five import monotonic
from functools import wraps

cache = Cache(app, config={"CACHE_TYPE": "redis"})
LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes

@contextmanager
def memcache_lock(lock_id, oid):
	timeout_at = monotonic() + LOCK_EXPIRE - 3
	print('in memcache_lock and timeout_at is {}'.format(timeout_at))
	# cache.add fails if the key already exists
	status = cache.add(lock_id, oid, LOCK_EXPIRE)
	try:
		yield status
		print('memcache_lock and status is {}'.format(status))
	finally:
		# memcache delete is very slow, but we have to use it to take
		# advantage of using add() for atomic locking
		if monotonic() < timeout_at and status:
			# don't release the lock if we exceeded the timeout
			# to lessen the chance of releasing an expired lock
			# owned by someone else
			# also don't release the lock if we didn't acquire it
			cache.delete(lock_id)


def requires_lock(fun):
	@wraps(fun)
	def outer(self, *args, **kwargs):
		lock_id = "global_db_lock"
		print("Obtaining lock...")
		with memcache_lock("lock_id", self.app.oid) as acquired:
			print('in memcache_lock and lock_id is {} self.app.oid is {} and acquired is {}'.format(lock_id, self.app.oid, acquired))
			if acquired:
				return fun(self, *args, **kwargs)

		raise TaskError("Unable to perform task")

	return outer


@celery.task(bind=True)
@requires_lock
def syncMusic(self):
	importAllMusic()

@celery.task(bind=True)
@requires_lock
def syncArtists(self):
	getArtistsInfo()

@celery.task(bind=True)
@requires_lock
def syncAlbums(self):
	getAlbumsInfo()
