<!-- ======================/ Template ====================== -->
<template>
    <div id="app">
        <div class="mb-3">
            <div class="mb-1">Select document</div>
            <input type="file" @change="on_file_selected" />
        </div>
        <div class="document-types mb-3">
            <div class="mb-1">Select correct tylpess document type name</div>
            <div v-if="existing_document_types">
                <div @click="selected_document_type = document_type.document_type_name" class="document-type clickable" :class="{ 'document-type-unselected': document_type.document_type_name !== selected_document_type }" v-for="document_type in existing_document_types" v-bind:key="document_type.id">{{ document_type.document_type_name }}</div>
            </div>
        </div>
        <div class="mb-3">
            <div class="btn btn-outline-primary w-100 process-btn" style="position: relative" @click="process_file">
                <div>Process</div>
                <div v-if="processing" class="spinner-border spinner-border-sm text-primary" style="margin-left: 5px; position: relative" role="status"></div>
            </div>
        </div>
        <div class="d-flex mt-5 row">
            <!-- ============== Saved documents list ============== -->
            <div class="document-list col-md">
                <h2>Saved documents</h2>
                <p v-if="!saved_documents?.length">Currently no documents to show.</p>
                <div class="document" v-else v-for="document in saved_documents" v-bind:key="document.id" @click="view_document(document)">
                    <div>{{ document.file_name }}</div>
                    <div class="document-type">{{ document.document_type_name }}</div>
                    <div>{{ get_local_datetime_string(document.timestamp) }}</div>
                </div>
            </div>
            <!-- ==============/ Saved documents list ============== -->

            <!-- ============== Document viewer ============== -->
            <div class="document-viewer col-md">
                <h2>Document viewer</h2>
                <template v-if="!document_viewer?.json">
                    <p>Open a saved document or process a new document.</p>
                </template>
                <template v-else>
                    <div class="document-viewer-info">
                        <div>
                            <h3>Document name:</h3>
                            {{ document_viewer.name }}
                        </div>
                        <div>
                            <h3>Document type name:</h3>
                            <div class="document-type">{{ document_viewer.document_type_name }}</div>
                        </div>
                        <div v-if="document_viewer.already_saved">
                            <h3>Saved on:</h3>
                            {{ get_local_datetime_string(document_viewer.timestamp) }}
                        </div>
                        <button v-else class="btn btn-sm btn-outline-primary" @click="save_response">Save response</button>
                        <h3 class="mt-3">Extracted data:</h3>
                    </div>
                    <pre class="response-json">{{ document_viewer.json }}</pre>
                </template>
            </div>
            <!-- ==============/ Document viewer ============== -->
        </div>
    </div>
</template>
<!-- ======================/ Template ====================== -->

<!-- ====================== Script ====================== -->
<script>
//insert_document
import { get_all_document_type_names, insert_document, get_all_documents, extract_data_from_document } from "../services/api";
import { use_toastr } from "../services/toast";

const toastr = use_toastr();

export default {
    name: "Manage_documents",
    props: {},

    data: function () {
        return {
            processing: false,
            saved_documents: null,
            existing_document_types: null,
            selected_document_type: null,
            document_viewer: {
                name: null,
                document_type_name: null,
                timestamp: null,
                json: null,
                already_saved: false,
            },
        };
    },
    computed: {},

    created: async function () {
        // Load existing documents from database
        this.load_documents();
        // Get all existing types
        this.load_document_types();
    },

    methods: {
        get_local_datetime_string(timestamp) {
            const date = new Date(timestamp * 1000).toLocaleString();
            return date;
        },

        view_document(document) {
            this.document_viewer.name = document.file_name;
            this.document_viewer.document_type_name = document.document_type_name;
            this.document_viewer.timestamp = document.timestamp;
            this.document_viewer.json = JSON.parse(document.json_string);
            this.document_viewer.already_saved = true;
        },

        on_file_selected(event) {
            this.file_selected = event.target.files[0];
        },

        // ============= Working with document types =============
        async load_document_types() {
            const response = await get_all_document_type_names();
            if (response.successful) {
                this.existing_document_types = response.data;
            } else {
                toastr.error(response.msg);
            }
        },
        // =============/ Working with document types =============

        // ============= Working with documents =============
        async load_documents() {
            const response = await get_all_documents();
            if (response.successful) {
                this.saved_documents = response.data;
            } else {
                toastr.error(response.msg);
            }
        },

        async save_response() {
            if (!this.document_viewer?.json) {
                toastr.warning("You dont have the json.");
                return;
            }

            // Call the api
            const response = await insert_document(this.document_viewer.name, this.document_viewer.document_type_name, this.document_viewer.json);

            // Check the response and inform the user
            if (response.successful) {
                // Update the fields in the viewer
                this.document_viewer.timestamp = response.data.timestamp;
                this.document_viewer.already_saved = true;
                // Insert into saved documents list
                this.saved_documents.push(response.data);

                toastr.success(response.msg);
            } else {
                toastr.error(response.msg);
            }
        },

        async process_file() {
            // Check if the user selected the document type name
            if (!this.selected_document_type) {
                toastr.warning("Please select a document type name.");
                return;
            }
            // Check if file is present and check if its one of the accepted formats
            const accepted_extensions = ["jpg", "png", "pdf"];
            if (!this.file_selected || !accepted_extensions.includes(this.file_selected.name.split(".").pop())) {
                toastr.warning("Please provide a PDF, JPG or PNG document.");
                return;
            }
            // Call the api
            this.processing = true;
            const response = await extract_data_from_document(this.file_selected, this.file_selected.name, this.selected_document_type);
            this.processing = false;

            // Check the response and inform the user
            if (response.successful) {
                // Set the document_viewer object
                this.document_viewer.name = this.file_selected.name;
                this.document_viewer.document_type_name = "api_test";
                this.document_viewer.timestamp = null;
                this.document_viewer.json = response.data;
                this.document_viewer.already_saved = false;

                toastr.success(response.msg);
            } else {
                toastr.error(response.msg);
            }
        },
        // =============/ Working with documents =============
    },
};
</script>
<!-- ======================/ Script ====================== -->

<!-- ====================== CSS ====================== -->
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h2 {
    font-size: medium;
}

.process-btn {
    position: relative;
    display: flex;
    justify-content: center;
}

.process-btn div:nth-child(2) {
    top: 4px;
}

.clickable:hover {
    cursor: pointer;
}

.document-types div {
    display: flex;
}

.document-types div > div:not(:first-child) {
    margin-left: 10px;
}

.document-type {
    padding: 0px 5px;
    width: fit-content;
    color: white;
    border-radius: 5px;
    background-color: #0d6efd;
    border: solid 1px #0d6efd;
    font-size: small;
    align-self: center;
}
.document-type-unselected {
    color: #0d6efd;
    background-color: white;
}

.document-list {
    width: 50vw;
    height: 60vh;
    overflow-x: auto;
    margin-right: 20px;
    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
    border-radius: 5px;
}

.document-list > p {
    font-size: small;
    margin-left: 10px;
}

.document {
    display: flex;
    width: max-content;
    margin: 5px 5px;
    padding: 2px 5px;
    box-shadow: rgba(0, 0, 0, 0.02) 0px 1px 3px 0px, rgba(27, 31, 35, 0.15) 0px 0px 0px 1px;
    border-radius: 3px;
    transition: margin 0.1s ease;
}

.document > div:not(:first-child) {
    margin-left: 10px;
}

.document:hover {
    cursor: pointer;
    margin-left: 10px;
}

.document-viewer {
    width: 50vw;
    height: 60vh;
    box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
    border-radius: 5px;
}

.document-viewer-info {
    margin-left: 10px;
}
.document-viewer-info > div {
    display: flex;
    align-items: center;
}
.document-viewer-info h3 {
    font-size: small;
    margin-bottom: 0px;
    margin-right: 10px;
}
.document-viewer > p {
    font-size: small;
    margin-left: 10px;
}

.response-json {
    margin: 10px 10px;
    padding: 20px 20px;
    max-height: 450px;
    overflow: auto;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 5px;
}
</style>
<!-- ======================/ CSS ====================== -->
