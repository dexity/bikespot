

window.views = {}

// Table row
views.DirectionStep = Backbone.View.extend({
    tagName: 'tr',
    initialize: function(options){
        _.bindAll(this, "render");
        this.model.bind('change', this.render);
    },
    render: function(){
        $(this.el).empty(); // Empty previous data
        $(this.el).append($('<td>' + this.model.get('step') + '.</td>'));
        $(this.el).append($('<td>' + this.model.get('direction') + '</td>'));
        $(this.el).append($('<td>' + this.model.get('distance') + '</td>'));
        $(this.el).append($('<td>' + this.model.get('duration') + '</td>'));
        return this;
    }
});

// Table view
views.DirectionView = Backbone.View.extend({
    collection: null,
    el: 'tbody',

    initialize: function(options){

        this.collection = options.collection;
        _.bindAll(this, "render");
        this.collection.bind('reset', this.render);
        this.collection.bind('add', this.render);
        this.collection.bind('remove', this.render);
        this.collection.bind('error', this.error);
    },
    error: function(xhr, data){
        $("#error").removeClass("hide").html(data.responseText);
    },
    render: function(){
        $("#error").removeClass("hide").addClass("hide");
        $("#directions").removeClass("hide");

        var elem = $(this.el);
        elem.empty();

        this.collection.forEach(function(item){
            var rowView = new views.DirectionStep({
                model: item
            });
            elem.append(rowView.render().el);
        });
        this.collection.drawPath(parking_map); // Draw path on the map

        return this;
    }
});

$(function(){

    // Request geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(successLocation, errorLocation);
    }

    window.AppView = Backbone.View.extend({
        el: 'body',
        events: {
            "click #parkme": "parkme"
        },
        initialize: function(){
            this.directions = new models.DirectionList;
            var view = new views.DirectionView({
                collection: this.directions
            });
        },
        parkme: function(){
            this.directions.url = directionsUrl(curr_lat, curr_lng);
            this.directions.fetch();    // Fetch directions
        }
    });

    window.App = new window.AppView;
})