

// Receive a string from frame.js
self.addEventListener('message', function (event) {
    //     if (event.origin != "https://our hosting provider") return;
    console.log("wikiTrustAlgo", wikiTrustAlgo);
    console.log("Worker data received from the iframe: ", event.data);

    self.postMessage(event.data);
}, false);



//     fetch("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donald_Trump&rvslots=*&rvlimit=50&rvstart=2013-07-01T00:00:00Z&rvprop=content&formatversion=2&format=json&origin=*").then((response) => {
//         response.json().then((obj) => {
//             let revisionsStripped = [];
//             console.log(obj)
//             console.log("body content: ", obj.query.pages[0].revisions[0].slots.main.content)
//             let revisions = obj.query.pages[0].revisions
//             for (var i = 0, len = obj.query.pages[0].revisions.length; i < len; i++) {
//                 let strippedText = module.parse_wiki_text(revisions[i].slots.main.content);
//                 revisionsStripped.push(strippedText);
//                 console.log("revison" + i, strippedText);
//             }
//             window.output = wikiTrustAlgo.getTrustExample(revisionsStripped);
//             autorun();
//         })
//     })

//     const getColorForPercentage = (pct, opacity) => { // Source: https://stackoverflow.com/questions/7128675/from-green-to-red-color-depend-on-percentage
//         const percentColorsGradient = [ // Define a gradient (0 = least trustworthy color, 1 = most trustworthy color)
//             { pct: 0.0, color: { r: 0xfc, g: 0x4a, b: 0x1a } }, // #fc4a1a
//             { pct: 0.5, color: { r: 0xf7, g: 0xb7, b: 0x33 } }, // #f7b733
//             { pct: 1.0, color: { r: 0xff, g: 0xff, b: 0xff } }  // white
//         ];
//         for (var i = 1; i < percentColorsGradient.length - 1; i++) {
//             if (pct < percentColorsGradient[i].pct) {
//                 break;
//             }
//         }
//         const lower = percentColorsGradient[i - 1];
//         const upper = percentColorsGradient[i];
//         const range = upper.pct - lower.pct;
//         const rangePct = (pct - lower.pct) / range;
//         const pctLower = 1 - rangePct;
//         const pctUpper = rangePct;
//         const color = {
//             r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
//             g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
//             b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
//         };
//         return `rgba(${[color.r, color.g, color.b, opacity].join(',')})`;
//         // or output as hex if preferred
//     };

//     var currentVersion = 0, globalMax = 0;

//     let updateBody = (wordList) => {
//         let container = document.getElementById("Text_Container");
//         container.innerHTML = ""; // clear old elements;


//         document.getElementById("info_area").innerText = "Current Version Index: " + currentVersion;
//         document.getElementById("gradient_max").innerText = globalMax;
//         wordList.forEach(function (word) {
//             let wordElem = document.createElement("span")
//             wordElem.innerText = word.text;
//             wordElem.style.borderBottom = `1px solid ${getColorForPercentage(word.trust / globalMax, 1)}`;
//             wordElem.style.backgroundColor = getColorForPercentage(word.trust / globalMax, 0.1);
//             wordElem.onmouseover = () => {
//                 // console.log()
//                 document.getElementById("gradient_marker").style.left = window.innerWidth * (word.trust / globalMax) + "px";
//                 document.getElementById("trust_score").innerText = "Trust Score: " + word.trust + " -- Max Trust Scaled: " + (word.trust / globalMax)
//             }
//             container.appendChild(wordElem)
//             container.appendChild(document.createTextNode(" "))
//         })
//     }

//     let findGlobalMax = () => {
//         var max = 0;
//         output.forEach((version) => {
//             version.forEach((word) => {
//                 if (word.trust > max) max = word.trust;
//             })
//         })
//         return max;
//     }

//     let keyDownHandle = (e) => {
//         e = e || window.event;

//         if (e.keyCode == '37') {
//             // left arrow
//             currentVersion--;
//             if (currentVersion < 0) currentVersion = 0;
//             updateBody(output[currentVersion])
//         }
//         else if (e.keyCode == '39') {
//             // right arrow
//             currentVersion++;
//             if (currentVersion == output.length) currentVersion = output.length - 1;
//             updateBody(output[currentVersion])
//         }
//     }

//     let autorun = () => {
//         currentVersion = output.length - 1;
//         globalMax = findGlobalMax();
//     }

// }).catch(console.error);
