class Response {
    constructor(successful = false, msg = "", data = null) {
        this.successful = successful;
        this.msg = msg;
        this.data = data;
    }
}

export { Response };
