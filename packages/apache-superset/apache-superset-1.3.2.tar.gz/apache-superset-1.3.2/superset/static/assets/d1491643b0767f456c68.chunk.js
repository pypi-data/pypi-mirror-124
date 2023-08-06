(window.webpackJsonp=window.webpackJsonp||[]).push([[33],{1930:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2287)).default;t.default=s},1931:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2288)).default;t.default=s},1932:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2289)).default;t.default=s},2287:function(e,t){e.exports=function(e){const t={begin:"<",end:">",subLanguage:"xml",relevance:0},a={begin:"\\[.+?\\][\\(\\[].*?[\\)\\]]",returnBegin:!0,contains:[{className:"string",begin:"\\[",end:"\\]",excludeBegin:!0,returnEnd:!0,relevance:0},{className:"link",begin:"\\]\\(",end:"\\)",excludeBegin:!0,excludeEnd:!0},{className:"symbol",begin:"\\]\\[",end:"\\]",excludeBegin:!0,excludeEnd:!0}],relevance:10},n={className:"strong",contains:[],variants:[{begin:/_{2}/,end:/_{2}/},{begin:/\*{2}/,end:/\*{2}/}]},s={className:"emphasis",contains:[],variants:[{begin:/\*(?!\*)/,end:/\*/},{begin:/_(?!_)/,end:/_/,relevance:0}]};n.contains.push(s),s.contains.push(n);var i=[t,a];return n.contains=n.contains.concat(i),s.contains=s.contains.concat(i),{name:"Markdown",aliases:["md","mkdown","mkd"],contains:[{className:"section",variants:[{begin:"^#{1,6}",end:"$",contains:i=i.concat(n,s)},{begin:"(?=^.+?\\n[=-]{2,}$)",contains:[{begin:"^[=-]*$"},{begin:"^",end:"\\n",contains:i}]}]},t,{className:"bullet",begin:"^[ \t]*([*+-]|(\\d+\\.))(?=\\s+)",end:"\\s+",excludeEnd:!0},n,s,{className:"quote",begin:"^>\\s+",contains:i,end:"$"},{className:"code",variants:[{begin:"(`{3,})(.|\\n)*?\\1`*[ ]*"},{begin:"(~{3,})(.|\\n)*?\\1~*[ ]*"},{begin:"```",end:"```+[ ]*$"},{begin:"~~~",end:"~~~+[ ]*$"},{begin:"`.+?`"},{begin:"(?=^( {4}|\\t))",contains:[{begin:"^( {4}|\\t)",end:"(\\n)$"}],relevance:0}]},{begin:"^[-\\*]{3,}",end:"$"},a,{begin:/^\[[^\n]+\]:/,returnBegin:!0,contains:[{className:"symbol",begin:/\[/,end:/\]/,excludeBegin:!0,excludeEnd:!0},{className:"link",begin:/:\s*/,end:/$/,excludeBegin:!0}]}]}}},2288:function(e,t){function a(...e){return e.map(e=>{return(t=e)?"string"==typeof t?t:t.source:null;var t}).join("")}e.exports=function(e){const t=function(e){const t={"builtin-name":["action","bindattr","collection","component","concat","debugger","each","each-in","get","hash","if","in","input","link-to","loc","log","lookup","mut","outlet","partial","query-params","render","template","textarea","unbound","unless","view","with","yield"].join(" ")},n={literal:["true","false","undefined","null"].join(" ")},s=/\[.*?\]/,i=/[^\s!"#%&'()*+,.\/;<=>@\[\\\]^`{|}~]+/,r=a("(",/'.*?'/,"|",/".*?"/,"|",s,"|",i,"|",/\.|\//,")+"),c=a("(",s,"|",i,")(?==)"),l={begin:r,lexemes:/[\w.\/]+/},o=e.inherit(l,{keywords:n}),d={begin:/\(/,end:/\)/},u={className:"attr",begin:c,relevance:0,starts:{begin:/=/,end:/=/,starts:{contains:[e.NUMBER_MODE,e.QUOTE_STRING_MODE,e.APOS_STRING_MODE,o,d]}}},b={contains:[e.NUMBER_MODE,e.QUOTE_STRING_MODE,e.APOS_STRING_MODE,{begin:/as\s+\|/,keywords:{keyword:"as"},end:/\|/,contains:[{begin:/\w+/}]},u,o,d],returnEnd:!0},g=e.inherit(l,{className:"name",keywords:t,starts:e.inherit(b,{end:/\)/})});d.contains=[g];const j=e.inherit(l,{keywords:t,className:"name",starts:e.inherit(b,{end:/}}/})}),m=e.inherit(l,{keywords:t,className:"name"}),h=e.inherit(l,{className:"name",keywords:t,starts:e.inherit(b,{end:/}}/})});return{name:"Handlebars",aliases:["hbs","html.hbs","html.handlebars","htmlbars"],case_insensitive:!0,subLanguage:"xml",contains:[{begin:/\\\{\{/,skip:!0},{begin:/\\\\(?=\{\{)/,skip:!0},e.COMMENT(/\{\{!--/,/--\}\}/),e.COMMENT(/\{\{!/,/\}\}/),{className:"template-tag",begin:/\{\{\{\{(?!\/)/,end:/\}\}\}\}/,contains:[j],starts:{end:/\{\{\{\{\//,returnEnd:!0,subLanguage:"xml"}},{className:"template-tag",begin:/\{\{\{\{\//,end:/\}\}\}\}/,contains:[m]},{className:"template-tag",begin:/\{\{#/,end:/\}\}/,contains:[j]},{className:"template-tag",begin:/\{\{(?=else\}\})/,end:/\}\}/,keywords:"else"},{className:"template-tag",begin:/\{\{(?=else if)/,end:/\}\}/,keywords:"else if"},{className:"template-tag",begin:/\{\{\//,end:/\}\}/,contains:[m]},{className:"template-variable",begin:/\{\{\{/,end:/\}\}\}/,contains:[h]},{className:"template-variable",begin:/\{\{/,end:/\}\}/,contains:[h]}]}}(e);return t.name="HTMLbars",e.getLanguage("handlebars")&&(t.disableAutodetect=!0),t}},2289:function(e,t){e.exports=function(e){var t={literal:"true false null"},a=[e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE],n=[e.QUOTE_STRING_MODE,e.C_NUMBER_MODE],s={end:",",endsWithParent:!0,excludeEnd:!0,contains:n,keywords:t},i={begin:"{",end:"}",contains:[{className:"attr",begin:/"/,end:/"/,contains:[e.BACKSLASH_ESCAPE],illegal:"\\n"},e.inherit(s,{begin:/:/})].concat(a),illegal:"\\S"},r={begin:"\\[",end:"\\]",contains:[e.inherit(s)],illegal:"\\S"};return n.push(i,r),a.forEach((function(e){n.push(e)})),{name:"JSON",contains:n,keywords:t,illegal:"\\S"}}},4697:function(e,t,a){"use strict";a.d(t,"a",(function(){return s}));var n=a(13);const s={name:Object(n.e)("Data"),tabs:[{name:"Databases",label:Object(n.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(n.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(n.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(n.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},4767:function(e,t,a){"use strict";a.d(t,"a",(function(){return w}));var n=a(25),s=a.n(n),i=(a(0),a(40)),r=a(13),c=a(641),l=a.n(c),o=a(1931),d=a.n(o),u=a(1930),b=a.n(u),g=a(1932),j=a.n(g),m=a(524),h=a.n(m),O=a(359),p=a.n(O),y=a(31),x=a(326),f=a(1);p.a.registerLanguage("sql",l.a),p.a.registerLanguage("markdown",b.a),p.a.registerLanguage("html",d.a),p.a.registerLanguage("json",j.a);const v=i.g.div`
  margin-top: -24px;

  &:hover {
    svg {
      visibility: visible;
    }
  }

  svg {
    position: relative;
    top: 40px;
    left: 512px;
    visibility: hidden;
    margin: -4px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`;function w({addDangerToast:e,addSuccessToast:t,children:a,...n}){return Object(f.jsx)(v,null,Object(f.jsx)(y.a.Copy,{tabIndex:0,role:"button",onClick:n=>{var s;n.preventDefault(),n.currentTarget.blur(),s=a,Object(x.a)(s).then(()=>{t&&t(Object(r.e)("SQL Copied!"))}).catch(()=>{e&&e(Object(r.e)("Sorry, your browser does not support copying."))})}}),Object(f.jsx)(p.a,s()({style:h.a},n),a))}},4768:function(e,t,a){"use strict";a.d(t,"a",(function(){return r}));a(41);var n=a(637),s=a.n(n),i=a(0);function r({queries:e,fetchData:t,currentQueryId:a}){const n=s()(e).call(e,e=>e.id===a),[r,c]=Object(i.useState)(n),[l,o]=Object(i.useState)(!1),[d,u]=Object(i.useState)(!1);function b(){o(0===r),u(r===e.length-1)}function g(a){const n=r+(a?-1:1);n>=0&&n<e.length&&(t(e[n].id),c(n),b())}return Object(i.useEffect)(()=>{b()}),{handleKeyPress:function(t){r>=0&&r<e.length&&("ArrowDown"===t.key||"k"===t.key?(t.preventDefault(),g(!1)):"ArrowUp"!==t.key&&"j"!==t.key||(t.preventDefault(),g(!0)))},handleDataChange:g,disablePrevious:l,disableNext:d}}},5076:function(e,t,a){"use strict";a.r(t);a(41);var n=a(11),s=a.n(n),i=a(0),r=a.n(i),c=a(40),l=a(13),o=a(66),d=a(37),u=a.n(d),b=a(117),g=a(142),j=a(418),m=a(720),h=a(144),O=a(4697),p=a(4669),y=a(51),x=a(359),f=a.n(x),v=a(641),w=a.n(v),_=a(524),k=a.n(_),S=a(104),N=a(417),q=a(31),C=a(114),$=a(5),E=a.n($),D=a(45),M=a(4767),T=a(4768),L=a(1);const H=c.g.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  margin-bottom: 0;
  text-transform: uppercase;
`,z=c.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m-1}px;
  padding: 4px 0 24px 0;
`,U=c.g.div`
  margin: 0 0 ${({theme:e})=>6*e.gridUnit}px 0;
`,R=c.g.div`
  display: inline;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding: ${({theme:e})=>2*e.gridUnit}px
    ${({theme:e})=>4*e.gridUnit}px;
  margin-right: ${({theme:e})=>4*e.gridUnit}px;
  color: ${({theme:e})=>e.colors.secondary.dark1};

  &.active,
  &:focus,
  &:hover {
    background: ${({theme:e})=>e.colors.secondary.light4};
    border-bottom: none;
    border-radius: ${({theme:e})=>e.borderRadius}px;
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  &:hover:not(.active) {
    background: ${({theme:e})=>e.colors.secondary.light5};
  }
`,A=Object(c.g)(C.b)`
  .ant-modal-body {
    padding: ${({theme:e})=>6*e.gridUnit}px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`;var B=Object(g.a)((function({onHide:e,openInSqlLab:t,queries:a,query:n,fetchData:s,show:r,addDangerToast:c,addSuccessToast:o}){const{handleKeyPress:d,handleDataChange:u,disablePrevious:b,disableNext:g}=Object(T.a)({queries:a,currentQueryId:n.id,fetchData:s}),[j,m]=Object(i.useState)("user"),{id:h,sql:O,executed_sql:p}=n;return Object(L.jsx)("div",{role:"none",onKeyUp:d},Object(L.jsx)(A,{onHide:e,show:r,title:Object(l.e)("Query preview"),footer:[Object(L.jsx)(D.a,{key:"previous-query",disabled:b,onClick:()=>u(!0)},Object(l.e)("Previous")),Object(L.jsx)(D.a,{key:"next-query",disabled:g,onClick:()=>u(!1)},Object(l.e)("Next")),Object(L.jsx)(D.a,{key:"open-in-sql-lab",buttonStyle:"primary",onClick:()=>t(h)},Object(l.e)("Open in SQL Lab"))]},Object(L.jsx)(H,null,Object(l.e)("Tab name")),Object(L.jsx)(z,null,n.tab_name),Object(L.jsx)(U,null,Object(L.jsx)(R,{role:"button",className:E()({active:"user"===j}),onClick:()=>m("user")},Object(l.e)("User query")),Object(L.jsx)(R,{role:"button",className:E()({active:"executed"===j}),onClick:()=>m("executed")},Object(l.e)("Executed query"))),Object(L.jsx)(M.a,{addDangerToast:c,addSuccessToast:o,language:"sql"},("user"===j?O:p)||"")))}));const I=Object(c.g)(p.b)`
  table .table-cell {
    vertical-align: top;
  }
`;f.a.registerLanguage("sql",w.a);const Q=Object(c.g)(f.a)`
  height: ${({theme:e})=>26*e.gridUnit}px;
  overflow: hidden !important; /* needed to override inline styles */
  text-overflow: ellipsis;
  white-space: nowrap;
`,P=c.g.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,F=c.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`;t.default=Object(g.a)((function({addDangerToast:e,addSuccessToast:t}){const{state:{loading:a,resourceCount:n,resourceCollection:d},fetchData:g}=Object(j.k)("query",Object(l.e)("Query history"),e,!1),[x,f]=Object(i.useState)(),v=Object(c.i)(),w=Object(i.useCallback)(t=>{o.a.get({endpoint:`/api/v1/query/${t}`}).then(({json:e={}})=>{f({...e.result})},Object(b.e)(t=>e(Object(l.e)("There was an issue previewing the selected query. %s",t))))},[e]),_={activeChild:"Query history",...O.a},C=[{id:N.a.start_time,desc:!0}],$=Object(i.useMemo)(()=>[{Cell:({row:{original:{status:e}}})=>{const t={name:null,label:""};return"success"===e?(t.name=Object(L.jsx)(q.a.Check,{iconColor:v.colors.success.base}),t.label=Object(l.e)("Success")):"failed"===e||"stopped"===e?(t.name=Object(L.jsx)(q.a.XSmall,{iconColor:"failed"===e?v.colors.error.base:v.colors.grayscale.base}),t.label=Object(l.e)("Failed")):"running"===e?(t.name=Object(L.jsx)(q.a.Running,{iconColor:v.colors.primary.base}),t.label=Object(l.e)("Running")):"timed_out"===e?(t.name=Object(L.jsx)(q.a.Offline,{iconColor:v.colors.grayscale.light1}),t.label=Object(l.e)("Offline")):"scheduled"!==e&&"pending"!==e||(t.name=Object(L.jsx)(q.a.Queued,{iconColor:v.colors.grayscale.base}),t.label=Object(l.e)("Scheduled")),Object(L.jsx)(y.a,{title:t.label,placement:"bottom"},Object(L.jsx)("span",null,t.name))},accessor:N.a.status,size:"xs",disableSortBy:!0},{accessor:N.a.start_time,Header:Object(l.e)("Time"),size:"xl",Cell:({row:{original:{start_time:e,end_time:t}}})=>{const a=u.a.utc(e).local().format(S.c).split(" "),n=Object(L.jsx)(r.a.Fragment,null,a[0]," ",Object(L.jsx)("br",null),a[1]);return t?Object(L.jsx)(y.a,{title:Object(l.e)("Duration: %s",u()(u.a.utc(t-e)).format(S.f)),placement:"bottom"},Object(L.jsx)("span",null,n)):n}},{accessor:N.a.tab_name,Header:Object(l.e)("Tab name"),size:"xl"},{accessor:N.a.database_name,Header:Object(l.e)("Database"),size:"xl"},{accessor:N.a.database,hidden:!0},{accessor:N.a.schema,Header:Object(l.e)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=s()(e).call(e,e=>e.table),a=t.length>0?t.shift():"";return t.length?Object(L.jsx)(P,null,Object(L.jsx)("span",null,a),Object(L.jsx)(h.a,{placement:"right",title:Object(l.e)("TABLES"),trigger:"click",content:Object(L.jsx)(r.a.Fragment,null,s()(t).call(t,e=>Object(L.jsx)(F,{key:e},e)))},Object(L.jsx)("span",{className:"count"},"(+",t.length,")"))):a},accessor:N.a.sql_tables,Header:Object(l.e)("Tables"),size:"xl",disableSortBy:!0},{accessor:N.a.user_first_name,Header:Object(l.e)("User"),size:"xl",Cell:({row:{original:{user:e}}})=>e?`${e.first_name} ${e.last_name}`:""},{accessor:N.a.user,hidden:!0},{accessor:N.a.rows,Header:Object(l.e)("Rows"),size:"md"},{accessor:N.a.sql,Header:Object(l.e)("SQL"),Cell:({row:{original:e,id:t}})=>Object(L.jsx)("div",{tabIndex:0,role:"button",onClick:()=>f(e)},Object(L.jsx)(Q,{language:"sql",style:k.a},Object(b.r)(e.sql,4)))},{Header:Object(l.e)("Actions"),id:"actions",disableSortBy:!0,Cell:({row:{original:{id:e}}})=>Object(L.jsx)(y.a,{title:Object(l.e)("Open query in SQL Lab"),placement:"bottom"},Object(L.jsx)("a",{href:`/superset/sqllab?queryId=${e}`},Object(L.jsx)(q.a.Full,{iconColor:v.colors.grayscale.base})))}],[]),E=Object(i.useMemo)(()=>[{Header:Object(l.e)("Database"),id:"database",input:"select",operator:p.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(b.g)("query","database",Object(b.e)(t=>e(Object(l.e)("An error occurred while fetching database values: %s",t)))),paginate:!0},{Header:Object(l.e)("State"),id:"status",input:"select",operator:p.a.equals,unfilteredLabel:"All",fetchSelects:Object(b.f)("query","status",Object(b.e)(t=>e(Object(l.e)("An error occurred while fetching schema values: %s",t)))),paginate:!0},{Header:Object(l.e)("User"),id:"user",input:"select",operator:p.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(b.g)("query","user",Object(b.e)(t=>e(Object(l.e)("An error occurred while fetching database values: %s",t)))),paginate:!0},{Header:Object(l.e)("Time range"),id:"start_time",input:"datetime_range",operator:p.a.between},{Header:Object(l.e)("Search by query text"),id:"sql",input:"search",operator:p.a.contains}],[e]);return Object(L.jsx)(r.a.Fragment,null,Object(L.jsx)(m.a,_),x&&Object(L.jsx)(B,{onHide:()=>f(void 0),query:x,queries:d,fetchData:w,openInSqlLab:e=>window.location.assign(`/superset/sqllab?queryId=${e}`),show:!0}),Object(L.jsx)(I,{className:"query-history-list-view",columns:$,count:n,data:d,fetchData:g,filters:E,initialSort:C,loading:a,pageSize:25,highlightRowId:null==x?void 0:x.id}))}))}}]);