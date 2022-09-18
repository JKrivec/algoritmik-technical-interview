<template>
    <Manage_documents />
</template>

<script>
import Manage_documents from "./components/Manage_documents.vue";

export default {
    name: "App",
    components: {
        Manage_documents,
    },
};
</script>

<style>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin: 60px 20px;
}
</style>
