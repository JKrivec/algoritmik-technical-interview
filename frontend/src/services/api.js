import { Response } from "@/models/response";
const axios = require("axios");

// Set the default axios URL to call (read from .env file)
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

async function get_all_strings() {
    return axios({
        method: "get",
        url: "strings",
    })
        .then((resp) => {
            return new Response(true, resp.msg, resp.data);
        })
        .catch((err) => {
            console.log("Error in api.js -> ", err);
            return new Response(false, err.message, null);
        });
}

export { get_all_strings };
