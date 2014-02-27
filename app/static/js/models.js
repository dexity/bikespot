
window.models = {}

models.Direction = Backbone.Model.extend({
    draw: function(map){
        drawStep(map, this.get("polyline"));
    }
});

models.DirectionList = Backbone.Collection.extend({
    model:  models.Direction,
    url:    directionsUrl(curr_lat, curr_lng),
    parse:  function(data, xhr){
        this.setTotal(data.meta);
        return data.directions;
    },
    setTotal: function(meta){
        var total_text = $.tmpl($("#total-tmpl").template(), meta).html();
        $("#total").html(total_text);
    },
    drawPath: function(map){
        for (var i=0; i<this.models.length; i++){
            this.models[i].draw(map)
        }
    }
});


