import { Response } from "@/models/response";
const axios = require("axios");

// Set the default axios URL to call (read from .env file)
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

async function get_all_documents() {
    return axios({
        method: "get",
        url: "documents",
    })
        .then((resp) => {
            return new Response(true, resp.msg, resp.data);
        })
        .catch((err) => {
            console.log("Error in api.js -> ", err);
            return new Response(false, err.message, null);
        });
}

async function insert_document(file_name, document_type_name, json_string) {
    return axios({
        method: "post",
        url: "documents",
        data: {
            file_name: file_name,
            document_type_name: document_type_name,
            json_string: json_string,
        },
        headers: { "Content-Type": "application/json" },
    })
        .then((resp) => {
            return new Response(true, resp.msg, resp.data);
        })
        .catch((err) => {
            console.log("Error in api.js -> ", err);
            return new Response(false, err.message, null);
        });
}

async function extract_data_from_document(file, file_name, document_type_name) {
    var form_data = new FormData();
    form_data.append("file", file);
    form_data.append("file_name", file_name);
    form_data.append("document_type_name", document_type_name);

    return axios({
        method: "post",
        url: "process",
        data: form_data,
        headers: { "Content-Type": "multipart/form-data" },
    })
        .then((resp) => {
            return new Response(true, resp.data.msg, resp.data.data);
        })
        .catch((err) => {
            console.log("Error in api.js -> ", err);
            // Check if we have a defined response from our backend
            if (err?.response?.data?.msg) {
                return new Response(false, err.response.data.msg, null);
            }
            return new Response(false, "There was an error while processing your document.<br />Please check the console", null);
        });
}

export { insert_document, get_all_documents, extract_data_from_document };
