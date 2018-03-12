import flask


class FlaskHelpers(object):
    """
    Wrapping flask api functions.
    """

    def response(self, response, response_code=200):
        """
        Return a response code with a custom response code.

        :param response:
            The response object.

        :param response_code:
            The response code for the page.

        :return:
        """
        return flask.jsonify(response), response_code

    def message(self, message, response_code=200):
        """
        A function to return a response with a simple message. If you need a more complex response use self.response()

        :param message:
            The message of the request.
        :param response_code:
            The response code for the page.

        :return:
        """
        return self.response({'message': message}, response_code)

    def error(self, error):
        """
        Print an error.

        :param error:
            The error.

        :return:
        """
        return self.response({'error': error}, 400)
