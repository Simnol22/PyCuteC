from Widgets.DataWidget import DataWidget
from Widgets.PrintWidget import PrintWidget
from Widgets.CompassWidget import CompassWidget
from Widgets.TerminalWidget import TerminalWidget
from Widgets.GroupWidget import GroupWidget
from Widgets.ChartWidget import ChartWidget

class WidgetFactory:
    def __init__(self, parent):
        self.widgets = {}
        # Important to have a reference to  the view, so that we can register the widgets
        # to the data transfer
        self.view = parent

    def buildAll(self, config, grid, parent = None):
        #Get the widgets from the config file
        for widgetConfig in config["widgets"]:
            #Check required fields
            if widgetConfig.get("x") is not None and widgetConfig.get("y") is not None:
                widget = self.buildWidget(widgetConfig, parent)
                if widget:
                    #Register widget to data transfer
                    self.view.registerWidget(widget)

                    #Add widget to the grid
                    xspan,yspan = 1,1
                    if widgetConfig.get("xspan"):
                        xspan = widgetConfig["xspan"]
                    if widgetConfig.get("yspan"):
                        yspan = widgetConfig["yspan"]
                
                    grid.addWidget(widget, widgetConfig["x"], widgetConfig["y"],xspan,yspan)

                    #Set the size of the widget if specified might want to use setMinimumSize instead here.
                    if widgetConfig.get("width"):
                        widget.setFixedWidth(widgetConfig["width"])
                    if widgetConfig.get("height"):
                         widget.setFixedWidth(widgetConfig["width"])
            else:
                if widgetConfig.get("type"):
                    print("Widget", widgetConfig["type"], "has no x or y value")
                else:
                    print("Unknown widget has no x or y value")
                


    def buildWidget(self, config, parent= None):
        #Check if the widget has a type
        if (config.get("type")):
            if config["type"] == "PrintWidget":
                return self.buildPrintWidget(config, parent)
            elif config["type"] == "DataWidget":
                return self.buildDataWidget(config, parent)
            elif config["type"] == "CompassWidget":
                return self.buildCompassWidget(config, parent)
            elif config["type"] == "TerminalWidget":
                return self.buildTerminalWidget(config, parent)
            elif config["type"] == "GroupWidget":
                return self.buildGroupWidget(config, parent)
            elif config["type"] == "ChartWidget":
                return self.buildChartWidget(config, parent)
            else:
                print("Widget type", config["type"]," not found")
                return None
            
        else:
            print("Widget has no type")
            return None
    
    def buildGroupWidget(self, config, parent):
        if not config.get("label"):
            print("GroupWidget has no label")
            return None
        if not config.get("widgets"):
            print("GroupWidget has no widgets")
            return None
        name = config.get("label")
        widget = GroupWidget(parent, name)
        self.buildAll(config, widget.grid, widget)
        return widget
    
    def buildDataWidget(self, config, parent):
        if not (config.get("label") or config.get("source")):
            print ("DataWidget has no label or source")
            return None
        widget = DataWidget(parent)
        widget.setLabel(config["label"])
        widget.setSource(config["source"])
        if config.get("unit"):
            widget.setUnit(config["unit"])
        if config.get("round") is not None:
            widget.setRounding(config["round"])
        return widget
    
    def buildPrintWidget(self, config, parent):
        widget = PrintWidget(parent)
        return widget
    
    def buildCompassWidget(self, config, parent):
        widget = CompassWidget(parent)
        return widget
    
    def buildTerminalWidget(self, config, parent):
        if not (config.get("label") or config.get("source")):
            print ("DataWidget has no label or source")
            return None
        widget = TerminalWidget(parent)
        widget.setLabel(config["label"])
        widget.setSource(config["source"])
        if config.get("round") is not None:
            widget.setRounding(config["round"])
        return widget
    
    def buildChartWidget(self, config, parent):
        if not (config.get("source")):
            print ("ChartWidget has no source")
            return None
        widget = ChartWidget(parent)
        widget.setSource(config["source"])
        if config.get("title") is not None:
            widget.setTitle(config["title"])
        return widget