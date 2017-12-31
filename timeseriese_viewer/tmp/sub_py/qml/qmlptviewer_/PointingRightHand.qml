import QtQuick 2.6
import QtQuick.Window 2.2

Canvas {
    id : pointing
    anchors.fill: parent

    onPaint: {
        var ctx = getContext("2d");
        ctx.fillStyle = Qt.rgba(1, 0, 0, 1);
        ctx.beginPath();
        ctx.arc(125, 300, 50, 0, Math.PI * 2, false);
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
