import QtQuick 2.6
import QtQuick.Window 2.2
import QtQuick.Controls 1.4

Rectangle {
    visible: true
    width: 400
    height: 500
    Canvas {
        id : bodyParts
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d");
            ctx.lineWidth = 5
            ctx.strokeStyle = "black"
            ctx.fillStyle = Qt.rgba(1, 1, 1, 1);

            ctx.beginPath()
            ctx.arc(200, 100, 45, 0, Math.PI * 2, false) //Head
            ctx.moveTo(150, 300)
            ctx.arc(125, 300, 20, 0, Math.PI * 2, false) //RightHand
            ctx.moveTo(295, 300)
            ctx.arc(275, 300, 20, 0, Math.PI * 2, false) //LeftHand
            ctx.closePath()

            ctx.stroke()
            ctx.strokeRect(150, 150, 100, 150)
            ctx.strokeRect(100, 150, 50, 125) //RightArm
            ctx.strokeRect(250, 150, 50, 125) //LeftArm
            ctx.strokeRect(150, 300, 50, 150)
            ctx.strokeRect(200, 300, 50, 150)
        }
    }
    PointingRightHand{}
}
