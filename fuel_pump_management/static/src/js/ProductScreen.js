odoo.define('fuel_pump_management.ProductScreen', function(require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    const ProductScreenExtend = (ProductScreen) =>
        class extends ProductScreen {
            _onClickPay() {
                if (this.env.pos.pump_ids){
                    let productIds = [];
                    const order = this.env.pos.get_order();
                    const orderlines = order.get_orderlines();
                    if(orderlines && orderlines.length) {
                        orderlines.forEach(orderline => {
                            if(orderline.product && orderline.product.id) {
                                productIds.push(orderline.product.id);
                            }
                        });
                    }
                    

                    let pumpFTIds = [];
                    const pumps = this.env.pos.pump_ids;
                    pumps.forEach(pump => {
                        if(pump.fuel_type && pump.fuel_type[0]) {
                            pumpFTIds.push(pump.fuel_type[0]);
                        }
                    });
                    pumpFTIds = pumpFTIds.filter((it, i, ar) => ar.indexOf(it) === i);


                    const commonIds = productIds.filter(value => pumpFTIds.includes(value));
                    if(commonIds && commonIds.length) {
                        // const selectedNozzle = order.changed && order.changed.nozzle_id;
                        const selectedNozzle = this.env.pos && this.env.pos.get_nozzle()
                        if(selectedNozzle) {
                            if(productIds.indexOf(selectedNozzle.fuel_type[0]) !== -1) {
                                console.log("Yes, nozzle selected!!");
                                this.showScreen('PaymentScreen');
                            } else {
                                this.showPopup('ErrorPopup', {
                                    title: this.env._t('Nozzle'),
                                    body: this.env._t("Please select correct nozzle!"),
                                });
                                return;
                                // alert("please select correct nozzle!");
                            }
                        }  else {
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Nozzle should be selected'),
                                body: this.env._t("Please select nozzle!"),
                            });
                            return;
                            // alert("please select nozzle!");
                        }
                    } else {
                        this.showScreen('PaymentScreen');
                    }
                } else {
                    this.showScreen('PaymentScreen');
                }

                
            }
        };

    Registries.Component.extend(ProductScreen, ProductScreenExtend);

    return ProductScreen;

});
