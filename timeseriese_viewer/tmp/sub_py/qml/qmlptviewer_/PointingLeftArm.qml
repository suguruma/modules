import QtQuick 2.6
import QtQuick.Window 2.2

Canvas {
    id : pointing
    anchors.fill: parent

    onPaint: {
        var ctx = getContext("2d");
        ctx.fillStyle = Qt.rgba(1, ColorLeftArm, 0, OnLeftArm);
        ctx.beginPath();
        ctx.ellipse(225, 125, 100, 175);
        ctx.fill();
        ctx.closePath()
    }

    NumberAnimation on opacity {
        id: fadeIn
        from : 0.1
        to: 0.9
        duration : 1000
        onRunningChanged: {
            if (!running) {
                fadeOut.start();
            }
        }
    }

    NumberAnimation on opacity {
        id: fadeOut
        from:0.9
        to: 0.1
        duration : 1000
        onRunningChanged: {
            if (!running) {
                fadeIn.start();
            }
        }
    }
}
