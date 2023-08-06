// Copyright 2018, National Technology & Engineering Solutions of Sandia, LLC
// (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
// Government retains certain rights in this software.

define([
    "debug",
    "knockout",
    "knockout.mapping",
    ], function(debug, ko, mapping)
{
    var log = debug("samlab-combo-control");

    var component_name = "samlab-combo-control";
    ko.components.register(component_name,
    {
        viewModel:
        {
            createViewModel: function(params, component_info)
            {
                var component = mapping.fromJS({
                    current: params.current,
                    disabled: params.disabled || false,
                    items: params.items,
                });

                component.expanded_items = component.items.map(function(item)
                {
                    return {extraclass: item.extraclass || "", divider: item.divider || false, heading: item.heading || false, icon: item.icon || "", key: item.key || "", label: item.label || "", shortcut: item.shortcut || ""};
                });

                component.current_item = ko.pureComputed(function()
                {
                    for(let item of component.expanded_items())
                    {
                        if(item.key() == component.current())
                        {
                            return item;
                        }
                    }
                });

                component.set_item = function(item)
                {
                    component.current(item.key());
                }

                return component;
            }
        },
        template: { require: "text!" + component_name + ".html" }
    });
});
