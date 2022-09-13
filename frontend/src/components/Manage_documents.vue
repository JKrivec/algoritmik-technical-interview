<!-- ======================/ Template ====================== -->
<template>
    <div id="app">
        <p>{{ greeting }}</p>
        <p>{{ flaskGreeting }}</p>
    </div>
</template>
<!-- ======================/ Template ====================== -->

<!-- ====================== Script ====================== -->
<script>
import { get_all_strings } from "../services/api";

export default {
    name: "Manage_documents",
    props: {},

    data: function () {
        return {
            greeting: "Hello, Vue!",
            flaskGreeting: "",
        };
    },

    computed: {
        console: () => console,
    },

    created: async function () {
        const response = await get_all_strings();
        console.log(response);
    },

    methods: {
        get_data: function () {
            return "data";
        },
    },
};
</script>
<!-- ======================/ Script ====================== -->

<!-- ====================== CSS ====================== -->
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
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
