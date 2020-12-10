import models

from flask import Blueprint, jsonify, request

from playhouse.shortcuts import model_to_dict

from flask_login import current_user, login_required
# We can use this as a Python decorator for routing purposes
# first argument is blueprints name
# second argument is it's import_name
walk = Blueprint('walks', 'walk')

#current directory is this '/api/v1/walks' for GET Routecd
@walk.route('/', methods=["GET"])
def get_all_walks():
    ## find the walks and change each one to a dictionary into a new array
    try:
        user = models.User.get_by_id(current_user.id)
        walks = [model_to_dict(walk) for walk in user.walks]

        print(current_user)
        #print(walks)
        return jsonify(data=walks, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

#Post Route (create)
@walk.route('/', methods=["POST"])
@login_required

def create_walks():
    ## see request payload anagolous to req.body in express
    payload = request.get_json()
    print(type(payload), 'payload')
    walk = models.Walk.create(name=payload['name'], author=current_user.id, tools=payload['tools'], materials=payload['materials'], edging=payload['edging'], path=payload['path'])
    ## see the object
    print(walk.__dict__)
    ## Look at all the methods
    print(dir(walk))
    # Change the model to a dict
    print(model_to_dict(walk), 'model to dict')
    walk_dict = model_to_dict(walk)
    return jsonify(data=walk_dict, status={"code": 201, "message": "Success"})

@walk.route('/<id>', methods=["GET"])
def get_one_walk(id):
    # print(id, 'reserved word?')
    walk = models.Walk.get_by_id(id)
    # print(walk.__dict__)
    return jsonify(data=model_to_dict(walk), status={"code": 200, "message": "Success"})



@walk.route('/<id>', methods=["PUT"])
def update_walk(id):
    payload = request.get_json()
    # print(payload)
    query = models.Walk.update(**payload).where(models.Walk.id==id)
    query.execute()
    walk = model_to_dict(models.Walk.get_by_id(id))
    return jsonify(data=walk, status={"code": 200, "message": "Success"})

@walk.route('/<id>', methods=["DELETE"])
def delete_walk(id):
    # we are trying to delete the walk with the id
    # check here for how: http://docs.peewee-orm.com/en/latest/peewee/querying.html#deleting-records
    delete_query = models.Walk.delete().where(models.Walk.id == id)
    num_of_rows_deleted = delete_query.execute()
    # print(num_of_rows_deleted)

    # todo: write logic -- if if no rows were deleted return
    # some message that delete didn't happen

    return jsonify(
    data={},
    message="Successfully deleted {} walk with id {}".format(num_of_rows_deleted, id),
    status={"code": 200}
    )
