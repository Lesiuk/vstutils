<template>
    <div class="container-fluid">
        <div class="row">
            <component
                :is="'field_' + field.options.format"
                v-for="(field, idx) in fieldsToShow"
                :key="idx"
                v-model="data_to_represent[field.options.name]"
                :field="field"
                :wrapper_opt="wrapper_opt"
                :prop_data="data_to_represent"
            />
        </div>
    </div>
</template>

<script>
    import $ from 'jquery';

    export default {
        name: 'filters_wrapper',
        props: ['view', 'opt', 'filters_data'],
        computed: {
            fieldsToShow() {
                return Object.values(this.filters).filter(
                    (field) => !(this.opt.hideReadOnly && field.options.readOnly),
                );
            },

            filters() {
                return this.view.schema.filters;
            },

            qs_url() {
                return this.opt.store_url;
            },

            data_to_represent() {
                return this.filters_data;
            },

            wrapper_opt() {
                return $.extend(true, {}, this.opt, { use_prop_data: true });
            },
        },
    };
</script>

<style scoped></style>
