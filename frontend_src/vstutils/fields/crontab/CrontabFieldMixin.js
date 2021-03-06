import { addCssClassesToElement } from '../../utils';
import { BaseFieldContentEdit } from '../base';
import CrontabFieldContentEdit from './CrontabFieldContentEdit.vue';

const CrontabFieldMixin = {
    data: function () {
        return {
            wrapper_classes_list: {
                base:
                    'form-group ' +
                    addCssClassesToElement(
                        'guiField',
                        this.field.options.name,
                        this.field.options.format || this.field.options.type,
                    ),
                grid: 'col-lg-12 col-xs-12 col-sm-12 col-md-12',
            },
        };
    },
    components: {
        field_content_edit: {
            mixins: [BaseFieldContentEdit, CrontabFieldContentEdit],
        },
    },
};

export default CrontabFieldMixin;
