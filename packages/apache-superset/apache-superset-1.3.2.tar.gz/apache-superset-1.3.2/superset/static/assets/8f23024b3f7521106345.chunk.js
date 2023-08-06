(window.webpackJsonp=window.webpackJsonp||[]).push([[88],{4668:function(t,e,a){"use strict";a.d(e,"a",(function(){return o})),a.d(e,"c",(function(){return i})),a.d(e,"b",(function(){return s}));var r=a(40),n=a(344);const o=r.g.div`
  min-height: ${({height:t})=>t}px;
  width: ${({width:t})=>t}px;
`,i=Object(r.g)(n.a)`
  &.ant-row.ant-form-item {
    margin: 0;
  }
`,s=r.g.div`
  color: ${({theme:t,status:e="error"})=>{var a;return null==(a=t.colors[e])?void 0:a.base}};
`},5024:function(t,e,a){"use strict";a.r(e),a.d(e,"default",(function(){return c}));var r=a(40),n=a(0),o=a(671),i=a(34),s=a(4668),u=a(1);const l=Object(r.g)(s.a)`
  overflow-x: auto;
`,d=r.g.div`
  padding: 2px;
  & > span,
  & > span:hover {
    border: 2px solid transparent;
    display: inline-block;
    border: ${({theme:t,validateStatus:e})=>{var a;return e&&`2px solid ${null==(a=t.colors[e])?void 0:a.base}`}};
  }
  &:focus {
    & > span {
      border: 2px solid
        ${({theme:t,validateStatus:e})=>{var a;return e?null==(a=t.colors[e])?void 0:a.base:t.colors.primary.base}};
      outline: 0;
      box-shadow: 0 0 0 2px
        ${({validateStatus:t})=>t?"rgba(224, 67, 85, 12%)":"rgba(32, 167, 201, 0.2)"};
    }
  }
`;function c(t){var e;const{setDataMask:a,setFocusedFilter:r,unsetFocusedFilter:s,width:c,height:v,filterState:b,formData:{inputRef:p}}=t,f=t=>{const e=t&&t!==i.k;a({extraFormData:e?{time_range:t}:{},filterState:{value:e?t:void 0}})};return Object(n.useEffect)(()=>{f(b.value)},[b.value]),null!=(e=t.formData)&&e.inView?Object(u.jsx)(l,{width:c,height:v},Object(u.jsx)(d,{tabIndex:-1,ref:p,validateStatus:b.validateStatus,onFocus:r,onBlur:s,onMouseEnter:r,onMouseLeave:s},Object(u.jsx)(o.a,{value:b.value||i.k,name:"time_range",onChange:f,type:b.validateStatus}))):null}}}]);