odoo.define('fuel_pump_management.SelectNozzleButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const useSelectNozzle = require('fuel_pump_management.useSelectNozzle')

    // Previously UsernameWidget
    class SelectNozzleButton extends PosComponent {
        constructor() {
            super(...arguments);
            const {selectNozzle} = useSelectNozzle();
            this.selectNozzle = selectNozzle;
        }
        mounted() {
            if (this.env.pos){
                this.env.pos.on('change:nozzle_id', this.render, this);
            }
            
        }
        willUnmount() {
            if (this.env.pos){
                this.env.pos.off('change:nozzle_id', null, this);
            }
        }

        get nozzlename() {
            if (this.env.pos){
                const cashier = this.env.pos.get_nozzle();
                if (cashier) {
                    return cashier.name;
                } 
            } else {
                return '';
            }
        }


        get currentOrder() {
            return this.env.pos.get_order();
        }

        async selectNozzles() {
            if (!this.env.pos.config.is_nozzle_used) return;
            const list = this.env.pos.pump_ids
                .filter((nozzle_id) => nozzle_id.id !== (this.env.pos.get_nozzle() && this.env.pos.get_nozzle().id))
                .map((nozzle_id) => {
                    return {
                        id: nozzle_id.id,
                        item: nozzle_id,
                        label: nozzle_id.name,
                        isSelected: false,
                    };
                });
            const nozzle_id = await this.selectNozzle(list);
            if (nozzle_id) {
                this.env.pos.set_nozzle(nozzle_id);
            }
        }
    }
    SelectNozzleButton.template = 'SelectNozzleButton';

    Registries.Component.add(SelectNozzleButton);

    return SelectNozzleButton;
});
