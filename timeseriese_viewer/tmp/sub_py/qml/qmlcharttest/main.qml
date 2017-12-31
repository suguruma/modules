import QtQuick 2.0
import QtCharts 2.0

ChartView {
    width: 300
    height: 350
    theme: ChartView.ChartThemeBrownSand
    antialiasing: true

    /*
    PolarChartView {
        title: "Timeserise Data Distance"
        anchors.fill: parent
        legend.visible: false
        antialiasing: true

        ValueAxis {
            id: axisAngular
            min: 0
            max: 20
            tickCount: 9
        }

        ValueAxis {
            id: axisRadial
            min: -0.5
            max: 1.5
        }

        SplineSeries {
            id: series1
            axisAngular: axisAngular
            axisRadial: axisRadial
            pointsVisible: true
        }

        ScatterSeries {
            id: series2
            axisAngular: axisAngular
            axisRadial: axisRadial
            markerSize: 10
        }
    }
    // Add data dynamically to the series
    Component.onCompleted: {
        for (var i = 0; i <= 20; i++) {
            series1.append(i, Math.random());
            series2.append(i, Math.random());
        }
    }*/
    /*
    PolarChartView {
        title: "Historical Area Series"
        anchors.fill: parent
        legend.visible: false
        antialiasing: true

        DateTimeAxis {
            id: axis1
            format: "yyyy MMM"
            tickCount: 13
        }
        ValueAxis {
            id: axis2
        }
        LineSeries {
            id: lowerLine
            axisAngular: axis1
            axisRadial: axis2

            // Please note that month in JavaScript months are zero based, so 2 means March
            XYPoint { x: toMsecsSinceEpoch(new Date(1950, 0, 1)); y: 15 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1962, 4, 1)); y: 35 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1970, 0, 1)); y: 50 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1978, 2, 1)); y: 75 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1987, 11, 1)); y: 102 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1992, 1, 1)); y: 132 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1998, 7, 1)); y: 100 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2002, 4, 1)); y: 120 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2012, 8, 1)); y: 140 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2013, 5, 1)); y: 150 }
        }
        LineSeries {
            id: upperLine
            axisAngular: axis1
            axisRadial: axis2

            // Please note that month in JavaScript months are zero based, so 2 means March
            XYPoint { x: toMsecsSinceEpoch(new Date(1950, 0, 1)); y: 30 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1962, 4, 1)); y: 55 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1970, 0, 1)); y: 80 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1978, 2, 1)); y: 105 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1987, 11, 1)); y: 125 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1992, 1, 1)); y: 160 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1998, 7, 1)); y: 140 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2002, 4, 1)); y: 140 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2012, 8, 1)); y: 170 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2013, 5, 1)); y: 200 }
        }
        AreaSeries {
            axisAngular: axis1
            axisRadial: axis2
            lowerSeries: lowerLine
            upperSeries: upperLine
        }
    }
    // DateTimeAxis is based on QDateTimes so we must convert our JavaScript dates to
    // milliseconds since epoch to make them match the DateTimeAxis values
    function toMsecsSinceEpoch(date) {
        var msecs = date.getTime();
        return msecs;
    }
    */
    PolarChartView {
        title: "Numerical Data for Dummies"
        anchors.fill: parent
        legend.visible: false
        antialiasing: true

        DateTimeAxis {
            id: axis1
            format: "yyyy MMM"
            tickCount: 13
        }
        ValueAxis {
            id: axis2
        }
        LineSeries {
            id: lowerLine
            axisAngular: axis1
            axisRadial: axis2

            // Please note that month in JavaScript months are zero based, so 2 means March
            XYPoint { x: toMsecsSinceEpoch(new Date(1950, 0, 1)); y: 15 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1962, 4, 1)); y: 35 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1970, 0, 1)); y: 50 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1978, 2, 1)); y: 75 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1987, 11, 1)); y: 102 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1992, 1, 1)); y: 132 }
            XYPoint { x: toMsecsSinceEpoch(new Date(1998, 7, 1)); y: 100 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2002, 4, 1)); y: 120 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2012, 8, 1)); y: 140 }
            XYPoint { x: toMsecsSinceEpoch(new Date(2013, 5, 1)); y: 150 }
        }
/*
        LineSeries {


            axisAngular: ValueAxis {
                tickCount: 15
            }

            XYPoint { x: 0; y: 29.3 } // = last value
            XYPoint { x: 1; y: 14.1 }
            XYPoint { x: 2; y: 14.7 }
            XYPoint { x: 3; y: 10.9 }
            XYPoint { x: 4; y: 13.2 }
            XYPoint { x: 5; y: 10.3 }
            XYPoint { x: 6; y: 16.1 }
            XYPoint { x: 7; y: 10.7 }
            XYPoint { x: 8; y: 12.9 }
            XYPoint { x: 9; y: 0.2 }
            XYPoint { x:10; y: 10.2 }
            XYPoint { x:11; y: 10 }
            XYPoint { x:12; y: 20.2 }
            XYPoint { x:13; y: 20.2 }
            XYPoint { x:14; y: 29.3 } // = first value
        }*/
    }
    function toMsecsSinceEpoch(date) {
        var msecs = date.getTime();
        return msecs;
    }

}

