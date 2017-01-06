/**
 * Created by jorik on 13-12-2016.
 */
function ShibaChef(x,y, width, height, texture) {
    PIXI.Sprite.call(this);

    //var self = this;

    this.texture = texture;

    //self.bounds = [];
    this.position.x = x;
    this.position.y = y;
    this.width = width;
    this.height = height;

    this.shibaStatus = 0; //0 = default, 1 = happy, 2 = angry
}

ShibaChef.prototype = new GameObject();
ShibaChef.prototype.constructor = ShibaChef;

ShibaChef.prototype.update = function() {
    switch (this.shibaStatus) {
        case 0:
            this.texture = PIXI.Texture.fromImage("shiba-neutral");
            break;
        case 1:
            this.texture = PIXI.Texture.fromImage("shiba-happy");
            break;
        case 2:
            this.texture = PIXI.Texture.fromImage("shiba-angry");
            break;
    }
};

ShibaChef.prototype.getAngory = function(duration) {
    this.shibaStatus = 2;
    var animation = null;
    if(Main.score.score <= -500) {
        animation = setInterval(function() {
            Main.shiba.rotation += Math.cos(new Date().getTime() * 0.2);
        }, 10);
    }
    setTimeout(function() {
        Main.shiba.shibaStatus = 0;
        //stop animation
        clearInterval(animation);
         Main.shiba.rotation = 0;
    }, duration);
};
ShibaChef.prototype.beHappy = function(duration) {
      this.shibaStatus = 1;
      setTimeout(function() {
          Main.shiba.shibaStatus = 0;
      }, duration);
};