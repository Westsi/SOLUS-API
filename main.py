from flask import Flask, jsonify, request, render_template
import json
import absolute_url

app = Flask('app')
app.config["DEBUG"] = True


# a placeholder welcome page
@app.route('/')
def hello_world():
    return render_template('index.html')


# to get all users via an api style method
@app.route('/api/v1/users/all', methods=['GET'])
def api_all_users():
    results = []
    # getting users from the list of users
    userf = open(absolute_url.ul_absolute, 'r')
    usernames = userf.readlines()
    userf.close()
    # looping through names and adding the corresponding files to the list to return
    for name in range(len(usernames)):
        fp = absolute_url.absolute_url + str(usernames[name][:-1]) + '.json'
        file = open(fp, 'r')
        userjson = file.read()
        userjson = json.loads(str(userjson))
        # instead of writing ones we do want, we remove ones we don't to future proof
        try:
            del userjson['Pass']
            del userjson['UUID']
            results.append(userjson)
        except KeyError:
            return 'There was an error. Please contact me.'

    return jsonify(results)


@app.route('/api/v1/users', methods=['GET'])
def api_id():
    # get id from url
    if 'id' in request.args:
        id = str(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    results = []
    # open list of users
    userf = open(absolute_url.ul_absolute, 'r')
    usernames = userf.readlines()
    userf.close()
    incn = 0
    if id in usernames:
        for user in usernames:
            if usernames[incn][:-1] == id:
                fileurl = absolute_url.absolute_url + str(usernames[incn][:-1]) + '.json'
                fspec = open(fileurl, 'r')
                specinfo = fspec.read()
                specinfo = json.loads(specinfo)
                del specinfo['Pass']
                del specinfo['UUID']
                results.append(specinfo)
            print(results)
            incn += 1
    else:
        return "User not found!"

    return jsonify(results)


app.run(host='0.0.0.0', port=8080)
