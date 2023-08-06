(window.webpackJsonp=window.webpackJsonp||[]).push([[89],{4668:function(t,e,a){"use strict";a.d(e,"a",(function(){return u})),a.d(e,"c",(function(){return s})),a.d(e,"b",(function(){return o}));var n=a(40),l=a(344);const u=n.g.div`
  min-height: ${({height:t})=>t}px;
  width: ${({width:t})=>t}px;
`,s=Object(n.g)(l.a)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,o=n.g.div`
  color: ${({theme:t,status:e="error"})=>{var a;return null==(a=t.colors[e])?void 0:a.base}};
`},5025:function(t,e,a){"use strict";a.r(e),a.d(e,"default",(function(){return p}));a(41);var n=a(25),l=a.n(n),u=a(11),s=a.n(u),o=a(35),r=a.n(o),c=a(64),i=a.n(c),d=a(230),h=a(227),f=a(13),v=a(0),b=a(212),g=a(4668),j=a(1);function p(t){var e;const{data:a,formData:n,height:u,width:o,setDataMask:c,setFocusedFilter:p,unsetFocusedFilter:m,filterState:w}=t,{defaultValue:O,inputRef:x}=n,[M,S]=Object(v.useState)(null!=O?O:[]),F=t=>{const e=Object(d.a)(t);S(e);const a={};e.length&&(a.granularity_sqla=e[0]),c({extraFormData:a,filterState:{value:e.length?e:null}})};Object(v.useEffect)(()=>{F(null!=O?O:null)},[i()(O)]),Object(v.useEffect)(()=>{var t;F(null!=(t=w.value)?t:null)},[i()(w.value)]);const E=r()(e=a||[]).call(e,t=>t.dtype===h.a.TEMPORAL),k=0===E.length?Object(f.e)("No time columns"):Object(f.f)("%s option","%s options",E.length,E.length),D={};w.validateMessage&&(D.extra=Object(j.jsx)(g.b,{status:w.validateStatus},w.validateMessage));const $=s()(E).call(E,t=>{const{column_name:e,verbose_name:a}=t;return{label:null!=a?a:e,value:e}});return Object(j.jsx)(g.a,{height:u,width:o},Object(j.jsx)(g.c,l()({validateStatus:w.validateStatus},D),Object(j.jsx)(b.a,{allowClear:!0,value:M,placeholder:k,onChange:F,onMouseEnter:p,onMouseLeave:m,ref:x,options:$})))}}}]);