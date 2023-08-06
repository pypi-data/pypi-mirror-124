(window.webpackJsonp=window.webpackJsonp||[]).push([[90],{4668:function(t,e,a){"use strict";a.d(e,"a",(function(){return o})),a.d(e,"c",(function(){return s})),a.d(e,"b",(function(){return u}));var n=a(40),l=a(344);const o=n.g.div`
  min-height: ${({height:t})=>t}px;
  width: ${({width:t})=>t}px;
`,s=Object(n.g)(l.a)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,u=n.g.div`
  color: ${({theme:t,status:e="error"})=>{var a;return null==(a=t.colors[e])?void 0:a.base}};
`},5027:function(t,e,a){"use strict";a.r(e),a.d(e,"default",(function(){return j}));a(41);var n=a(25),l=a.n(n),o=a(11),s=a.n(o),u=a(64),r=a.n(u),i=a(50),c=a.n(i),d=a(230),f=a(13),h=a(0),v=a(212),b=a(4668),g=a(1);function j(t){var e;const{data:a,formData:n,height:o,width:u,setDataMask:i,setFocusedFilter:j,unsetFocusedFilter:p,filterState:w}=t,{defaultValue:O,inputRef:m}=n,[x,M]=Object(h.useState)(null!=O?O:[]),S=Object(h.useMemo)(()=>c()(a).call(a,(t,{duration:e,name:a})=>({...t,[e]:a}),{}),[r()(a)]),F=t=>{const e=Object(d.a)(t),[a]=e,n=a?S[a]:void 0,l={};a&&(l.time_grain_sqla=a),M(e),i({extraFormData:l,filterState:{label:n,value:e.length?e:null}})};Object(h.useEffect)(()=>{F(null!=O?O:[])},[r()(O)]),Object(h.useEffect)(()=>{var t;F(null!=(t=w.value)?t:[])},[r()(w.value)]);const k=0===(a||[]).length?Object(f.e)("No data"):Object(f.f)("%s option","%s options",a.length,a.length),D={};w.validateMessage&&(D.extra=Object(g.jsx)(b.b,{status:w.validateStatus},w.validateMessage));const E=s()(e=a||[]).call(e,t=>{const{name:e,duration:a}=t;return{label:e,value:a}});return Object(g.jsx)(b.a,{height:o,width:u},Object(g.jsx)(b.c,l()({validateStatus:w.validateStatus},D),Object(g.jsx)(v.a,{allowClear:!0,value:x,placeholder:k,onChange:F,onMouseEnter:j,onMouseLeave:p,ref:m,options:E})))}}}]);