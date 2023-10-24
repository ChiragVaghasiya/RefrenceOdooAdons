odoo.define('fuel_pump_management.models', function (require) {
"use strict";
	var pos_models = require('point_of_sale.models');
	var posmodel_super = pos_models.PosModel.prototype;

	pos_models.load_models([{
	    model:  'pump.pump',
	    fields: ['name', 'sr_no', 'fuel_type', 'pos_config', 'company_id'],
	    domain: function(self) {
	    	return [['pos_config', '=', self.config_id || false]]
	    },
	    loaded: function(self, pump_ids) {
	        if (self.config.is_nozzle_used && (self.config.company_id[0] == self.config.nozzle_company[0])) {
	            self.pump_ids = pump_ids;
	            // self.nozzle_id = pump_ids[0];
	            self.pump_by_id = {};
	            self.pump_ids.forEach(function(pump) {
	                self.pump_by_id[pump.id] = pump;
	            });
	        }
	    }
	}]);

	pos_models.PosModel = pos_models.PosModel.extend({

		initialize: function () {
            var self = this;
         //    this.set({
	        //     'selectedNozzle':   null,
	        //     'nozzle_id':        null,
	        // });
            var res = posmodel_super.initialize.apply(this, arguments);
            return res;
        },

		load_pos_product_session_start: async function(category){
	        var self = this;
	        const result = await self.rpc({
                  model: 'pos.config',
                  method: 'check_products_in_category',
                  args: [self.config_id, category, self.config.nozzle_warehouse_id, self.pos_session.id],
            });
            return result
	    },

		after_load_server_data : async function(){
			var result = posmodel_super.after_load_server_data.apply(this, arguments);
			var self = this;
			if (this.config.nozzle_company && this.pos_session.state === 'opening_control'){
				_.each(this.product_categories, function (category) {
	                if (category.name === 'Fuel'){
	                	self.load_pos_product_session_start(category);

	                }
	            });

			}
			return result;

		},

		set_nozzle: function(val){
    		this.set('nozzle_id', val);
    		if (this.get_order()){
    			this.get_order().set_nozzle(val)
    		}
    	},

    	get_nozzle: function(){
    		return this.get('nozzle_id');
    	},
	});



	var _super = pos_models.Order;
    pos_models.Order = pos_models.Order.extend({

    	initialize: function (attributes, options) {
	        _super.prototype.initialize.apply(this, arguments);
	        this.set({ nozzle_id: null });
	    },

	    set_nozzle: function(val){
    		this.set('nozzle_id', val);
    	},

    	get_nozzle: function(){
    		return this.get('nozzle_id') || null;
    	},


    	init_from_JSON: function (json) {
	        _super.prototype.init_from_JSON.apply(this, arguments);
	        if (this.pos.config.is_nozzle_used && json.nozzle_id && (this.pos.config.company_id[0] == this.pos.config.nozzle_company[0])) {
	            this.nozzle_id = this.pos.pump_by_id[json.nozzle_id];
	        }
	    },
        
    	
	    export_as_JSON: function() {
            var self = this;
        	var new_val = {};
            var orders = _super.prototype.export_as_JSON.call(this);
            var nozzle_val = this.pos.get_nozzle()
            new_val = {
            	nozzle_id: nozzle_val ? nozzle_val.id : false,
            }
            $.extend(orders, new_val);
            return orders;
    	},
    	

    });

});

