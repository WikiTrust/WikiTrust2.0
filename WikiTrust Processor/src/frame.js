
//https://stackoverflow.com/questions/58598510/how-to-prevent-script-injection-attacks
//https://stackoverflow.com/questions/21692646/how-does-facebook-disable-the-browsers-integrated-developer-tools
/*
javascript:(function(){window.g=document.createElement("iframe");g.src="http://localhost:1234/src/frame.html";document.body.appendChild(g);console.log(g);window.addEventListener('message',(event)=>{console.log("Received_message_event_from_iframe_in_wikipedia:",event)},false);g.onload=()=>{g.contentWindow.postMessage("hi","http://localhost:1234/");}})()
g.contentWindow.postMessage("hi","http://localhost:1234/")
*/

const worker = new Worker('worker.js');

// Receive data from the web worker:
worker.addEventListener('message', (event) => {
    console.log("Data from worker received: ", event.data);
    console.log("Sending data to parent page (wikipdia page)...");
    parentPage.postMessage(event.data, "https://en.wikipedia.org"); // Send the message to the parent page.
}, true);

const parentPage = window.parent;

// Receive string from the parent page (wikipdia page):
window.addEventListener('message', (event) => {
    if (event.origin != "https://en.wikipedia.org") return;
    console.log("Received message event from parent page: ", JSON.parse(JSON.stringify(event)))
    console.log("Sending message to worker thread...")
    worker.postMessage(event.data); // Send the message to the web worker thread.
}, false);

// ---------- Go to Worker.js --------
import "regenerator-runtime/runtime.js";
import * as wikiTrustAlgo from './Python/__target__/demo.js';
import { parse_wiki_text } from './Rust/pkg/rust_webpack_template.js';

fetch("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donald_Trump&rvslots=*&rvlimit=50&rvstart=2013-07-01T00:00:00Z&rvprop=content&formatversion=2&format=json&origin=*").then((response) => {
    response.json().then((obj) => {
        console.log(obj)
        let revisionsStripped = [];
        let revisions = obj.query.pages[0].revisions
        for (var i = 0, len = revisions.length; i < len; i++) {
            const revisionId = revisions[i].slots.main.content
            const revisionUserId = revisions[i].slots.main.content
            const strippedText = parse_wiki_text(revisions[i].slots.main.content);
            const output = { "text": strippedText, "revisionId": revisionId, "userId": revisionUserId }
            revisionsStripped.push(output);
        }
        window.output = wikiTrustAlgo.getTrustExample({ "pageId": 123, "revisions": revisionsStripped, "size": revisionsStripped.length });
    })
})