class Storage {

    constructor() {
        let data = {};
        this.getItem = function (item) {
            return data[item];
        }

        this.getData = function () {
            return data;
        }


        this.setItem = function (item, value) {
            data[item] = value;
        }

        this.removeItem = function (item) {
            delete data.item;
        }
    }

}

const clientStorageProperties = {
    current_plan_name: "current_plan_name",
    current_day_selected: "current_day_selected",
    current_category_selected: "current_category_selected",
    selected_plans: "selected_plans",
    current_meal:"current_meal",
};
Object.freeze(clientStorageProperties);


(function(){
    this.clientStorage = new Storage();
})();