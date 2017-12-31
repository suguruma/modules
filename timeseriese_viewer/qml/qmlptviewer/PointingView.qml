import QtQuick 2.6
import QtQuick.Window 2.2

Canvas {
    id : pointing
    anchors.fill: parent

    onPaint: {
        // HandRight
        var ctx = getContext("2d");
        var frgba = strRGBASpliter(HandRight, ',')
        ctx.fillStyle = Qt.rgba(frgba[0], frgba[1], frgba[2], frgba[3]);
        ctx.beginPath();
        ctx.arc(125, 300, 50, 0, Math.PI * 2, false);
        ctx.fill();
        ctx.closePath()

        // HandLeft
        var ctx2 = getContext("2d");
        var frgba2 = strRGBASpliter(HandLeft, ',')
        ctx2.fillStyle = Qt.rgba(frgba2[0], frgba2[1], frgba2[2], frgba2[3]);
        ctx2.beginPath();
        ctx2.arc(275, 300, 50, 0, Math.PI * 2, false);
        ctx2.fill();
        ctx2.closePath()

        // Head
        var ctx3 = getContext("2d");
        var frgba3 = strRGBASpliter(Head, ',')
        ctx3.fillStyle = Qt.rgba(frgba3[0], frgba3[1], frgba3[2], frgba3[3]);
        ctx3.beginPath();
        ctx3.arc(200, 100, 75, 0, Math.PI * 2, false);
        ctx3.fill();
        ctx3.closePath()

        // ElbowLeft
        var ctx4 = getContext("2d");
        var frgba4 = strRGBASpliter(ElbowLeft, ',')
        ctx4.fillStyle = Qt.rgba(frgba4[0], frgba4[1], frgba4[2], frgba4[3]);
        ctx4.beginPath();
        ctx4.ellipse(225, 125, 100, 175);
        ctx4.fill();
        ctx4.closePath()

        // ElbowRight
        var ctx5 = getContext("2d");
        var frgba5 = strRGBASpliter(ElbowRight, ',')
        ctx5.fillStyle = Qt.rgba(frgba5[0], frgba5[1], frgba5[2], frgba5[3]);
        ctx5.beginPath();
        ctx5.ellipse(75, 125, 100, 175);
        ctx5.fill();
        ctx5.scale(2.0, 0.5);
        ctx5.closePath()

        function strRGBASpliter(strRGBA, splitter)
        {
            var spStrRGBA = strRGBA.split(splitter);
            var fRGBA = [parseFloat(spStrRGBA[0]), parseFloat(spStrRGBA[1]), parseFloat(spStrRGBA[2]), parseFloat(spStrRGBA[3])];
            return fRGBA;
        }
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
