<template>
    <div>
        <field_clear_button
            :field="field"
            @cleanValue="$emit('proxyEvent', 'cleanValue')"
        ></field_clear_button>

        <field_read_file_button
            :field="field"
            @readFile="$emit('proxyEvent', 'readFile', $event)"
        ></field_read_file_button>

        <field_hidden_button
            v-if="with_hidden_button"
            :field="field"
            @hideField="$emit('proxyEvent', 'hideField')"
        ></field_hidden_button>

        <textarea
            :value="value"
            @input="$emit('proxyEvent', 'setValueInStore', $event.target.value)"
            :placeholder="$t('enter value') | capitalize"
            :class="classes"
            :style="styles"
            :required="attrs['required']"
            :minlength="attrs['minlength']"
            :maxlength="attrs['maxlength']"
            :aria-labelledby="label_id"
            :aria-label="aria_label"
        ></textarea>
    </div>
</template>

<script>
    import { BaseFieldContentEdit, BaseFieldButton } from '../../base';
    import FileFieldButtonMixin from './FileFieldButtonMixin.js';
    import FileFieldReadFileButton from './FileFieldReadFileButton.vue';

    export default {
        mixins: [BaseFieldContentEdit],
        data() {
            return {
                styles_dict: { resize: 'vertical' },
            };
        },
        components: {
            field_clear_button: {
                mixins: [BaseFieldButton, FileFieldButtonMixin],
            },
            field_hidden_button: {
                mixins: [BaseFieldButton, FileFieldButtonMixin],
                data() {
                    return {
                        icon_classes: ['fa', 'fa-minus'],
                        event_handler: 'hideField',
                        help_text: 'Hide field',
                    };
                },
            },
            field_read_file_button: FileFieldReadFileButton,
        },
    };
</script>

<style scoped></style>
