<!-- ======================/ Template ====================== -->
<template>
    <div id="app">
        <p class="mt-5">{{ greeting }}</p>
        <div>
            <input type="file" @change="on_file_selected" />
        </div>
        <button class="btn btn-outline-primary" @click="process_file">Process</button>
        <button class="btn btn-outline-secondary" @click="save_response">Save response</button>
        <pre class="response-json">{{ current_response.json }}</pre>
    </div>
</template>
<!-- ======================/ Template ====================== -->

<!-- ====================== Script ====================== -->
<script>
//insert_document
import { insert_document, get_all_documents, extract_data_from_document } from "../services/api";
import { use_toastr } from "../services/toast";

const toastr = use_toastr();

export default {
    name: "Manage_documents",
    props: {},

    data: function () {
        return {
            greeting: "Hello, Vue!",
            current_response: {
                json: null,
                name: null,
                queried_document_type_name: null,
                already_saved: false,
            },
            file_selected: null,
        };
    },

    computed: {},

    created: async function () {
        const all_docs = await get_all_documents();
        console.log(all_docs);
    },

    methods: {
        get_data() {
            return "data";
        },
        on_file_selected(event) {
            this.file_selected = event.target.files[0];
        },

        async save_response() {
            if (!this.current_response?.json) {
                toastr.warning("You dont have the json.");
                return;
            }
            if (this.current_response.already_saved) {
                toastr.warning("Current response is already in the database.");
                return;
            }

            // Call the api
            const response = await insert_document(this.current_response.name, this.current_response.queried_document_type_name, this.current_response.json);

            // Check the response and inform the user
            if (response.successful) {
                console.log(response);
                this.current_response.json = response.data;
                toastr.success(response.msg);
            } else {
                toastr.error(response.msg);
            }
        },

        async process_file() {
            // Check if file is present and check if its one of the accepted formats
            const accepted_extensions = ["jpg", "png", "pdf"];
            if (!this.file_selected || !accepted_extensions.includes(this.file_selected.name.split(".").pop())) {
                toastr.warning("Please provide a PDF, JPG or PNG document.");
                return;
            }
            // Call the api
            const response = await extract_data_from_document(this.file_selected, this.file_selected.name, "api_test");

            // Check the response and inform the user
            if (response.successful) {
                // Set the current_response object
                this.current_response.json = response.data;
                this.current_response.name = this.file_selected.name;
                this.current_response.queried_document_type_name = "api_test";
                this.current_response.already_saved = false;

                toastr.success(response.msg);
            } else {
                toastr.error(response.msg);
            }
        },
    },
};
</script>
<!-- ======================/ Script ====================== -->

<!-- ====================== CSS ====================== -->
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.response-json {
    margin: 10px 10px;
    padding: 20px 20px;
    max-height: 400px;
    overflow: auto;
    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
}

h3 {
    margin: 40px 0 0;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: inline-block;
    margin: 0 10px;
}
a {
    color: #42b983;
}
</style>
<!-- ======================/ CSS ====================== -->
