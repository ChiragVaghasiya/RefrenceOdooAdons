odoo.define('fuel_pump_management.useSelectNozzle', function (require) {
    'use strict';

    const { Component } = owl;

    function useSelectNozzle() {
        const current = Component.current;

        async function selectNozzle(selectionList) {
            const { confirmed, payload: nozzle } = await this.showPopup('SelectionPopup', {
                title: this.env._t('Change Nozzle'),
                list: selectionList,
            });

            if (!confirmed) return false;

            return nozzle;
        }
        return { selectNozzle: selectNozzle.bind(current) };
    }

    return useSelectNozzle;
});
