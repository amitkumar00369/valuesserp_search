
const DynamicFields = (function () {
    let container = null;
    let minFields = 1;

    function createField(value = "") {
        const wrapper = document.createElement('div');
        wrapper.className = "mb-2 input-group";
        const input = document.createElement('input');
        input.type = "text";
        input.placeholder = "Enter search query";
        input.className = "form-control";
        input.value = value;
        wrapper.appendChild(input);
        return wrapper;
    }

    return {
        init: function (opts) {
            minFields = opts.minFields || 1;
            container = document.getElementById('fieldsContainer');
           
            if (!container.querySelector('input')) {
                container.appendChild(createField(''));
            }
            document.getElementById('addFieldBtn').addEventListener('click', () => {
                container.appendChild(createField(''));
            });
            document.getElementById('removeFieldBtn').addEventListener('click', () => {
                const inputs = container.querySelectorAll('.input-group');
                if (inputs.length > minFields) {
                    container.removeChild(inputs[inputs.length - 1]);
                }
            });
        },
        getValues: function () {
            if (!container) return [];
            const inputs = container.querySelectorAll('input');
            return Array.from(inputs).map(i => i.value);
        }
    }
})();