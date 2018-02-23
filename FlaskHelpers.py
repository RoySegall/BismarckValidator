import flask


class FlaskHelpers(object):
    """
    Wrapping flask api functions.
    """

    def response(self, response, response_code=200):
        """
        Return a response code with a custom response code.
        :param response:
        :param response_code:
        :return:
        """
        return flask.jsonify(response), response_code

    def message(self, message, response_code=200):
        """
        A function to return a response with a simple message. If you need a more complex response use self.response()
        :param message:
        :param response_code:
        :return:
        """
        return self.response({'message': message}, response_code)
