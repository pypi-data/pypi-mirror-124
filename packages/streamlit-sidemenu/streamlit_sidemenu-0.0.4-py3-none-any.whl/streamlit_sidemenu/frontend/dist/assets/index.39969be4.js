import{S as i}from"./vendor.90a306ac.js";const b=function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))l(e);new MutationObserver(e=>{for(const n of e)if(n.type==="childList")for(const a of n.addedNodes)a.tagName==="LINK"&&a.rel==="modulepreload"&&l(a)}).observe(document,{childList:!0,subtree:!0});function u(e){const n={};return e.integrity&&(n.integrity=e.integrity),e.referrerpolicy&&(n.referrerPolicy=e.referrerpolicy),e.crossorigin==="use-credentials"?n.credentials="include":e.crossorigin==="anonymous"?n.credentials="omit":n.credentials="same-origin",n}function l(e){if(e.ep)return;e.ep=!0;const n=u(e);fetch(e.href,n)}};b();const w=`
body {
  margin: 0;
}

#app {
  margin: 0;
}

/* Fixed sidenav, full height */
.sidenav {
  font-family: Arial;
  height: 100%;
  width: 100%;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  /* padding-top: 20px; */
}

/* Style the sidenav links and the dropdown button */
.sidenav a, .dropdown-btn {
  padding: 6px 8px 6px 16px;
  text-decoration: none;
  font-size: 20px;
  color: #818181;
  display: block;
  border: none;
  background: none;
  width:100%;
  text-align: left;
  cursor: pointer;
  outline: none;
}

/* On mouse-over */
.sidenav a:hover, .dropdown-btn:hover {
  color: #f1f1f1;
}

/* Main content */
.main {
  margin-left: 200px; /* Same as the width of the sidenav */
  font-size: 20px; /* Increased text to enable scrolling */
  padding: 0px 10px;
}

/* Add an active class to the active dropdown button */
.sidenav a.selected {
  background-color: green;
  color: white;
}

/* Dropdown container (hidden by default). Optional: add a lighter background color and some left padding to change the design of the dropdown content */
.dropdown-container {
  display: none;
  background-color: #262626;
  padding-left: 8px;
}

/* Optional: Style the caret down icon */
.fa-caret-down {
  float: right;
  padding-right: 8px;
}
`;function h(d){let t=d-280;t<0&&(t=240),document.getElementById("app").style.height=t+"px",i.setFrameHeight()}function v(d,t){console.log("sssssssssssssssssssssssssssssss"),i.setComponentValue({selected:d,opened:t})}function x(d){console.log("Render",d);const t=d.detail,u=t.args.items;let l=t.args.selected||"",e=t.args.opened||[];const n=t.args.styles||w,a=document.createElement("style");a.innerText=n,document.head.appendChild(a);const r=document.createElement("div");r.classList.add("sidenav");function f(o){const s=document.createElement("a");return l===o.label&&s.classList.add("selected"),s.onclick=()=>{l=o.label,v(l,e)},s.innerHTML=o.label,s}u.forEach(o=>{if(o.children){const s=document.createElement("button");s.classList.add("dropdown-btn"),s.innerHTML=o.label;const c=document.createElement("div");c.classList.add("dropdown-container"),e.includes(o.label)&&(c.style.display="block"),s.onclick=g=>{const p=c;p.style.display==="block"?(e=e.filter(y=>o.label!==y),console.log("aaa1",e),p.style.display="none"):(e.push(o.label),console.log("aaa2",e),p.style.display="block")},r.appendChild(s),o.children.forEach(g=>{const p=f(g);c.appendChild(p)}),r.appendChild(c)}else{const s=f(o);r.appendChild(s)}}),document.getElementById("app").appendChild(r),h(window.outerHeight),document.getElementById("app").style.overflow="auto",i.setFrameHeight()}i.events.addEventListener(i.RENDER_EVENT,x);i.setComponentReady();i.setFrameHeight();let m=null;window.parent.addEventListener("resize",function(){clearTimeout(m),m=setTimeout(()=>h(window.outerHeight),500)});
