
require("src/mapping.js")
var HelloWorldLayer = cc.Layer.extend({
    sprite:null,
    ctor:function () {
        //////////////////////////////
        // 1. super init first
        this._super();

        /////////////////////////////
        // 2. add a menu item with "X" image, which is clicked to quit the program
        //    you may modify it.
        // ask the window size
        var size = cc.winSize;

        /////////////////////////////
        // 3. add your codes below...
        // add a label shows "Hello World"
        // create and initialize a label
        var helloLabel = new cc.LabelTTF("Hello World", "Arial", 38);
        // position the label on the center of the screen
        helloLabel.x = size.width / 2;
        helloLabel.y = size.height / 2 + 200;
        // add the label as a child to this layer
        this.addChild(helloLabel, 5);

        // add "HelloWorld" splash screen"
        var path = this.getMappingPath(res.HelloWorld_png);
        this.sprite = new cc.Sprite(path);
        this.sprite.attr({
            x: size.width / 2,
            y: size.height / 2
        });
        this.addChild(this.sprite, 0);
                      
        return true;
    },

    getMappingPath: function(res)
    {
        cc.log("cyj = ", JSON.stringify(res_mapping));
        cc.log("1 = ", res, res_mapping[res]);
        var md51 = res_mapping[res].toString();
        cc.log("2 = ", md51);
        var dir = md51.substr(0,2);
        var png = md51.substr(2);
        var path = "res/" + dir +"/" + png + ".png";
        cc.log("path  = ", path);
        path = 'res/HelloWorld.png';
        return path;
    }
});

var HelloWorldScene = cc.Scene.extend({
    onEnter:function () {
        this._super();
        var layer = new HelloWorldLayer();
        this.addChild(layer);
    }
});

