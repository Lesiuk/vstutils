import $ from 'jquery';
import { FKField } from '../fk';
import FKAutocompleteFieldMixin from './FKAutocompleteFieldMixin.js';

/**
 * FK_autocomplete guiField class.
 */
class FKAutocompleteField extends FKField {
    constructor(options) {
        super(options);
        this._usePrefetch = false;
        this._fetchData = false;
    }

    /**
     * Redefinition of fk guiField method _insertTestValue.
     */
    _insertTestValue(data = {}) {
        let value = data[this.options.name];
        let format = this.options.format || this.options.type;
        let el = this._insertTestValue_getElement(format);

        $(el).val(value);

        this._insertTestValue_imitateEvent(el);
    }
    /**
     * Redefinition of fk guiField method _insertTestValue_getElement.
     */
    _insertTestValue_getElement(format) {
        let selector = '.guifield-' + format + '-' + this.options.name + ' input';
        return $(selector)[0];
    }
    /**
     * Redefinition of fk guiField method _insertTestValue_imitateEvent.
     */
    _insertTestValue_imitateEvent(el) {
        el.dispatchEvent(new Event('blur'));
    }
    /**
     * Redefinition of base guiField static property 'mixins'.
     */
    static get mixins() {
        return super.mixins.concat(FKAutocompleteFieldMixin);
    }
}

export default FKAutocompleteField;
