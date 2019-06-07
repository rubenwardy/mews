from flask import redirect, render_template, request
from app import app
from app.tasks import celery, TaskError
from app.utils import shouldReturnJSON
from flask_user import current_user

@app.route("/tasks/<id>/")
def check_task(id):
	result = celery.AsyncResult(id)
	status = result.status
	traceback = result.traceback
	result = result.result

	info = None
	if isinstance(result, Exception):
		info = {
				'id': id,
				'status': status,
			}

		if current_user.is_authenticated and current_user.is_admin:
			info["error"] = str(traceback)
		elif str(result)[1:12] == "TaskError: ":
			info["error"] = str(result)[12:-1]
		else:
			info["error"] = "Unknown server error"
	else:
		info = {
				'id': id,
				'status': status,
				'result': result,
			}

	if shouldReturnJSON():
		return jsonify(info)
	else:
		r = request.args.get("r")
		if r is not None and status == "SUCCESS":
			return redirect(r)
		else:
			return render_template("tasks/view.html", info=info)
