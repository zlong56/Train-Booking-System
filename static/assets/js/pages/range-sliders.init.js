if(! document.querySelectorAll("[data-rangeslider]").length == 0){
for (var sliderColorScheme = document.querySelectorAll("[data-rangeslider]"), multielementslider = (sliderColorScheme && Array.from(sliderColorScheme).forEach(function(e) {
        noUiSlider.create(e, {
            start: 127,
            connect: "lower",
            range: {
                min: 0,
                max: 255
            }
        })
    }), document.querySelectorAll("[data-multielement]")), resultElement = (multielementslider && Array.from(multielementslider).forEach(function(e) {
        noUiSlider.create(e, {
            start: [20, 80],
            connect: !0,
            range: {
                min: 0,
                max: 100
            }
        })
    }), document.getElementById("result")), sliders = document.getElementsByClassName("sliders"), colors = [0, 0, 0], select = (sliders && Array.from([].slice.call(sliders)).forEach(function(i, t) {
        noUiSlider.create(i, {
            start: 127,
            connect: [!0, !1],
            orientation: "vertical",
            range: {
                min: 0,
                max: 255
            },
            format: wNumb({
                decimals: 0
            })
        }), i.noUiSlider.on("update", function() {
            colors[t] = i.noUiSlider.get();
            var e = "rgb(" + colors.join(",") + ")";
            resultElement.style.background = e, resultElement.style.color = e
        })
    }), document.getElementById("input-select")), i = -20; i <= 40; i++) {
    var option = document.createElement("option");
    option.text = i, option.value = i, select.appendChild(option)
}
var html5Slider = document.getElementById("html5"),
    inputNumber = (html5Slider && noUiSlider.create(html5Slider, {
        start: [10, 30],
        connect: !0,
        range: {
            min: -20,
            max: 40
        }
    }), document.getElementById("input-number")),
    nonLinearSlider = (inputNumber && html5Slider && (html5Slider.noUiSlider.on("update", function(e, i) {
        e = e[i];
        i ? inputNumber.value = e : select.value = Math.round(e)
    }), select.addEventListener("change", function() {
        html5Slider.noUiSlider.set([this.value, null])
    }), inputNumber.addEventListener("change", function() {
        html5Slider.noUiSlider.set([null, this.value])
    })), document.getElementById("nonlinear")),
    nodes = (nonLinearSlider && noUiSlider.create(nonLinearSlider, {
        connect: !0,
        behaviour: "tap",
        start: [500, 4e3],
        range: {
            min: [0],
            "10%": [500, 500],
            "50%": [4e3, 1e3],
            max: [1e4]
        }
    }), [document.getElementById("lower-value"), document.getElementById("upper-value")]),
    lockedState = (nonLinearSlider.noUiSlider.on("update", function(e, i, t, n, l) {
        nodes[i].innerHTML = e[i] + ", " + l[i].toFixed(2) + "%"
    }), !1),
    lockedSlider = !1,
    lockedValues = [60, 80],
    slider1 = document.getElementById("slider1"),
    slider2 = document.getElementById("slider2"),
    lockButton = document.getElementById("lockbutton"),
    slider1Value = document.getElementById("slider1-span"),
    slider2Value = document.getElementById("slider2-span");

function crossUpdate(e, i) {
    var t;
    lockedState && (e -= lockedValues[(t = slider1 === i ? 0 : 1) ? 0 : 1] - lockedValues[t], i.noUiSlider.set(e))
}

function setLockedValues() {
    lockedValues = [Number(slider1.noUiSlider.get()), Number(slider2.noUiSlider.get())]
}
lockButton && lockButton.addEventListener("click", function() {
    lockedState = !lockedState, this.textContent = lockedState ? "unlock" : "lock"
}), noUiSlider.create(slider1, {
    start: 60,
    animate: !1,
    range: {
        min: 50,
        max: 100
    }
}), noUiSlider.create(slider2, {
    start: 80,
    animate: !1,
    range: {
        min: 50,
        max: 100
    }
}), slider1 && slider2 && (slider1.noUiSlider.on("update", function(e, i) {
    slider1Value.innerHTML = e[i]
}), slider2.noUiSlider.on("update", function(e, i) {
    slider2Value.innerHTML = e[i]
}), slider1.noUiSlider.on("change", setLockedValues), slider2.noUiSlider.on("change", setLockedValues), slider1.noUiSlider.on("slide", function(e, i) {
    crossUpdate(e[i], slider2)
}), slider2.noUiSlider.on("slide", function(e, i) {
    crossUpdate(e[i], slider1)
}));
var mergingTooltipSlider = document.getElementById("slider-merging-tooltips");

function mergeTooltips(e, c, m) {
    var u = "rtl" === getComputedStyle(e).direction,
        S = "rtl" === e.noUiSlider.options.direction,
        g = "vertical" === e.noUiSlider.options.orientation,
        p = e.noUiSlider.getTooltips(),
        t = e.noUiSlider.getOrigins();
    Array.from(p).forEach(function(e, i) {
        e && t[i].appendChild(e)
    }), e && e.noUiSlider.on("update", function(e, i, t, n, l) {
        var r = [
                []
            ],
            a = [
                []
            ],
            s = [
                []
            ],
            o = 0;
        p[0] && (r[0][0] = 0, a[0][0] = l[0], s[0][0] = e[0]);
        for (var d = 1; d < l.length; d++)(!p[d] || l[d] - l[d - 1] > c) && (r[++o] = [], s[o] = [], a[o] = []), p[d] && (r[o].push(d), s[o].push(e[d]), a[o].push(l[d]));
        Array.from(r).forEach(function(e, i) {
            for (var t = e.length, n = 0; n < t; n++) {
                var l, r, o, d = e[n];
                n === t - 1 ? (o = 0, Array.from(a[i]).forEach(function(e) {
                    o += 1e3 - e
                }), l = g ? "bottom" : "right", r = 1e3 - a[i][S ? 0 : t - 1], o = (u && !g ? 100 : 0) + o / t - r, p[d].innerHTML = s[i].join(m), p[d].style.display = "block", p[d].style[l] = o + "%") : p[d].style.display = "none"
            }
        })
    })
}
mergingTooltipSlider && (noUiSlider.create(mergingTooltipSlider, {
    start: [20, 75],
    connect: !0,
    tooltips: [!0, !0],
    range: {
        min: 0,
        max: 100
    }
}), mergeTooltips(mergingTooltipSlider, 5, " - "));
var hidingTooltipSlider = document.getElementById("slider-hide"),
    pipsSlider = (hidingTooltipSlider && noUiSlider.create(hidingTooltipSlider, {
        range: {
            min: 0,
            max: 100
        },
        start: [20, 80],
        tooltips: !0
    }), document.getElementById("slider-pips")),
    pips = (pipsSlider && noUiSlider.create(pipsSlider, {
        range: {
            min: 0,
            max: 100
        },
        start: [50],
        pips: {
            mode: "count",
            values: 5
        }
    }), pipsSlider.querySelectorAll(".noUi-value"));

function clickOnPip() {
    var e = Number(this.getAttribute("data-value"));
    pipsSlider.noUiSlider.set(e)
}
pips && Array.from(pips).forEach(function(e) {
    e.style.cursor = "pointer", e.addEventListener("click", clickOnPip)
});
var slider = document.getElementById("slider-color"),
    connect = (slider && noUiSlider.create(slider, {
        start: [4e3, 8e3, 12e3, 16e3],
        connect: [!1, !0, !0, !0, !0],
        range: {
            min: [2e3],
            max: [2e4]
        }
    }), slider.querySelectorAll(".noUi-connect")),
    classes = ["c-1-color", "c-2-color", "c-3-color", "c-4-color", "c-5-color"],
    i = 0,
    toggleSlider = (Array.from(connect).forEach(function(e) {
        e.classList.add(classes[i]), i++
    }), document.getElementById("slider-toggle")),
    softSlider = (toggleSlider && (noUiSlider.create(toggleSlider, {
        orientation: "vertical",
        start: 0,
        range: {
            min: [0, 1],
            max: 1
        },
        format: wNumb({
            decimals: 0
        })
    }), toggleSlider.noUiSlider.on("update", function(e, i) {
        "1" === e[i] ? toggleSlider.classList.add("off") : toggleSlider.classList.remove("off")
    })), document.getElementById("soft"));
softSlider && (noUiSlider.create(softSlider, {
    start: 50,
    range: {
        min: 0,
        max: 100
    },
    pips: {
        mode: "values",
        values: [20, 80],
        density: 4
    }
}), softSlider.noUiSlider.on("change", function(e, i) {
    e[i] < 20 ? softSlider.noUiSlider.set(20) : 80 < e[i] && softSlider.noUiSlider.set(80)
}));
}
