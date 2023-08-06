(window.webpackJsonp=window.webpackJsonp||[]).push([[34],{1930:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2287)).default;t.default=s},1931:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2288)).default;t.default=s},1932:function(e,t,a){"use strict";var n=a(8);Object.defineProperty(t,"__esModule",{value:!0}),t.default=void 0;var s=n(a(2289)).default;t.default=s},2287:function(e,t){e.exports=function(e){const t={begin:"<",end:">",subLanguage:"xml",relevance:0},a={begin:"\\[.+?\\][\\(\\[].*?[\\)\\]]",returnBegin:!0,contains:[{className:"string",begin:"\\[",end:"\\]",excludeBegin:!0,returnEnd:!0,relevance:0},{className:"link",begin:"\\]\\(",end:"\\)",excludeBegin:!0,excludeEnd:!0},{className:"symbol",begin:"\\]\\[",end:"\\]",excludeBegin:!0,excludeEnd:!0}],relevance:10},n={className:"strong",contains:[],variants:[{begin:/_{2}/,end:/_{2}/},{begin:/\*{2}/,end:/\*{2}/}]},s={className:"emphasis",contains:[],variants:[{begin:/\*(?!\*)/,end:/\*/},{begin:/_(?!_)/,end:/_/,relevance:0}]};n.contains.push(s),s.contains.push(n);var i=[t,a];return n.contains=n.contains.concat(i),s.contains=s.contains.concat(i),{name:"Markdown",aliases:["md","mkdown","mkd"],contains:[{className:"section",variants:[{begin:"^#{1,6}",end:"$",contains:i=i.concat(n,s)},{begin:"(?=^.+?\\n[=-]{2,}$)",contains:[{begin:"^[=-]*$"},{begin:"^",end:"\\n",contains:i}]}]},t,{className:"bullet",begin:"^[ \t]*([*+-]|(\\d+\\.))(?=\\s+)",end:"\\s+",excludeEnd:!0},n,s,{className:"quote",begin:"^>\\s+",contains:i,end:"$"},{className:"code",variants:[{begin:"(`{3,})(.|\\n)*?\\1`*[ ]*"},{begin:"(~{3,})(.|\\n)*?\\1~*[ ]*"},{begin:"```",end:"```+[ ]*$"},{begin:"~~~",end:"~~~+[ ]*$"},{begin:"`.+?`"},{begin:"(?=^( {4}|\\t))",contains:[{begin:"^( {4}|\\t)",end:"(\\n)$"}],relevance:0}]},{begin:"^[-\\*]{3,}",end:"$"},a,{begin:/^\[[^\n]+\]:/,returnBegin:!0,contains:[{className:"symbol",begin:/\[/,end:/\]/,excludeBegin:!0,excludeEnd:!0},{className:"link",begin:/:\s*/,end:/$/,excludeBegin:!0}]}]}}},2288:function(e,t){function a(...e){return e.map(e=>{return(t=e)?"string"==typeof t?t:t.source:null;var t}).join("")}e.exports=function(e){const t=function(e){const t={"builtin-name":["action","bindattr","collection","component","concat","debugger","each","each-in","get","hash","if","in","input","link-to","loc","log","lookup","mut","outlet","partial","query-params","render","template","textarea","unbound","unless","view","with","yield"].join(" ")},n={literal:["true","false","undefined","null"].join(" ")},s=/\[.*?\]/,i=/[^\s!"#%&'()*+,.\/;<=>@\[\\\]^`{|}~]+/,o=a("(",/'.*?'/,"|",/".*?"/,"|",s,"|",i,"|",/\.|\//,")+"),r=a("(",s,"|",i,")(?==)"),l={begin:o,lexemes:/[\w.\/]+/},c=e.inherit(l,{keywords:n}),d={begin:/\(/,end:/\)/},u={className:"attr",begin:r,relevance:0,starts:{begin:/=/,end:/=/,starts:{contains:[e.NUMBER_MODE,e.QUOTE_STRING_MODE,e.APOS_STRING_MODE,c,d]}}},b={contains:[e.NUMBER_MODE,e.QUOTE_STRING_MODE,e.APOS_STRING_MODE,{begin:/as\s+\|/,keywords:{keyword:"as"},end:/\|/,contains:[{begin:/\w+/}]},u,c,d],returnEnd:!0},g=e.inherit(l,{className:"name",keywords:t,starts:e.inherit(b,{end:/\)/})});d.contains=[g];const p=e.inherit(l,{keywords:t,className:"name",starts:e.inherit(b,{end:/}}/})}),m=e.inherit(l,{keywords:t,className:"name"}),j=e.inherit(l,{className:"name",keywords:t,starts:e.inherit(b,{end:/}}/})});return{name:"Handlebars",aliases:["hbs","html.hbs","html.handlebars","htmlbars"],case_insensitive:!0,subLanguage:"xml",contains:[{begin:/\\\{\{/,skip:!0},{begin:/\\\\(?=\{\{)/,skip:!0},e.COMMENT(/\{\{!--/,/--\}\}/),e.COMMENT(/\{\{!/,/\}\}/),{className:"template-tag",begin:/\{\{\{\{(?!\/)/,end:/\}\}\}\}/,contains:[p],starts:{end:/\{\{\{\{\//,returnEnd:!0,subLanguage:"xml"}},{className:"template-tag",begin:/\{\{\{\{\//,end:/\}\}\}\}/,contains:[m]},{className:"template-tag",begin:/\{\{#/,end:/\}\}/,contains:[p]},{className:"template-tag",begin:/\{\{(?=else\}\})/,end:/\}\}/,keywords:"else"},{className:"template-tag",begin:/\{\{(?=else if)/,end:/\}\}/,keywords:"else if"},{className:"template-tag",begin:/\{\{\//,end:/\}\}/,contains:[m]},{className:"template-variable",begin:/\{\{\{/,end:/\}\}\}/,contains:[j]},{className:"template-variable",begin:/\{\{/,end:/\}\}/,contains:[j]}]}}(e);return t.name="HTMLbars",e.getLanguage("handlebars")&&(t.disableAutodetect=!0),t}},2289:function(e,t){e.exports=function(e){var t={literal:"true false null"},a=[e.C_LINE_COMMENT_MODE,e.C_BLOCK_COMMENT_MODE],n=[e.QUOTE_STRING_MODE,e.C_NUMBER_MODE],s={end:",",endsWithParent:!0,excludeEnd:!0,contains:n,keywords:t},i={begin:"{",end:"}",contains:[{className:"attr",begin:/"/,end:/"/,contains:[e.BACKSLASH_ESCAPE],illegal:"\\n"},e.inherit(s,{begin:/:/})].concat(a),illegal:"\\S"},o={begin:"\\[",end:"\\]",contains:[e.inherit(s)],illegal:"\\S"};return n.push(i,o),a.forEach((function(e){n.push(e)})),{name:"JSON",contains:n,keywords:t,illegal:"\\S"}}},4681:function(e,t,a){"use strict";a.d(t,"a",(function(){return u}));var n=a(11),s=a.n(n),i=(a(0),a(40)),o=a(51),r=a(31),l=a(1);const c=i.g.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:e})=>e.colors.primary.base};
      }
    }
  }
`,d=i.g.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function u({actions:e}){return Object(l.jsx)(c,{className:"actions"},s()(e).call(e,(e,t)=>{const a=r.a[e.icon];return e.tooltip?Object(l.jsx)(o.a,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},Object(l.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},Object(l.jsx)(a,null))):Object(l.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},Object(l.jsx)(a,null))}))}},4682:function(e,t,a){"use strict";a(41);var n=a(11),s=a.n(n),i=a(35),o=a.n(i),r=a(0),l=a.n(r),c=a(40),d=a(13),u=a(45),b=a(114),g=a(19),p=a(418),m=a(1);const j=c.g.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,h=c.g.div`
  padding-bottom: ${({theme:e})=>2*e.gridUnit}px;
  padding-top: ${({theme:e})=>2*e.gridUnit}px;

  & > div {
    margin: ${({theme:e})=>e.gridUnit}px 0;
  }

  &.extra-container {
    padding-top: 8px;
  }

  .confirm-overwrite {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .input-container {
    display: flex;
    align-items: center;

    label {
      display: flex;
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }

    i {
      margin: 0 ${({theme:e})=>e.gridUnit}px;
    }
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }

  textarea,
  input[type='text'],
  input[type='number'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border-style: none;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;

    &[name='name'] {
      flex: 0 1 auto;
      width: 40%;
    }

    &[name='sqlalchemy_uri'] {
      margin-right: ${({theme:e})=>3*e.gridUnit}px;
    }
  }
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:n,addDangerToast:i,addSuccessToast:c,onModelImport:O,show:y,onHide:x,passwordFields:v=[],setPasswordFields:f=(()=>{})})=>{const[w,S]=Object(r.useState)(!0),[k,N]=Object(r.useState)({}),[_,E]=Object(r.useState)(!1),[C,q]=Object(r.useState)(!1),[D,$]=Object(r.useState)([]),[T,M]=Object(r.useState)(!1),I=()=>{$([]),f([]),N({}),E(!1),q(!1),M(!1)},{state:{alreadyExists:R,passwordsNeeded:L},importResource:B}=Object(p.j)(e,t,e=>{I(),i(e)});Object(r.useEffect)(()=>{f(L),L.length>0&&M(!1)},[L,f]),Object(r.useEffect)(()=>{E(R.length>0),R.length>0&&M(!1)},[R,E]);const H=e=>{var t,a;const n=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";q(n.toUpperCase()===Object(d.e)("OVERWRITE"))};return w&&y&&S(!1),Object(m.jsx)(b.b,{name:"model",className:"import-model-modal",disablePrimaryButton:0===D.length||_&&!C||T,onHandledPrimaryAction:()=>{var e;(null==(e=D[0])?void 0:e.originFileObj)instanceof File&&(M(!0),B(D[0].originFileObj,k,C).then(e=>{e&&(c(Object(d.e)("The import was successful")),I(),O())}))},onHide:()=>{S(!0),x(),I()},primaryButtonName:_?Object(d.e)("Overwrite"):Object(d.e)("Import"),primaryButtonType:_?"danger":"primary",width:"750px",show:y,title:Object(m.jsx)("h4",null,Object(d.e)("Import %s",t))},Object(m.jsx)(h,null,Object(m.jsx)(g.F,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:D,onChange:e=>{$([{...e.file,status:"done"}])},onRemove:e=>($(o()(D).call(D,t=>t.uid!==e.uid)),!1),customRequest:()=>{}},Object(m.jsx)(u.a,{loading:T},"Select file"))),0===v.length?null:Object(m.jsx)(l.a.Fragment,null,Object(m.jsx)("h5",null,"Database passwords"),Object(m.jsx)(j,null,a),s()(v).call(v,e=>Object(m.jsx)(h,{key:`password-for-${e}`},Object(m.jsx)("div",{className:"control-label"},e,Object(m.jsx)("span",{className:"required"},"*")),Object(m.jsx)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:k[e],onChange:t=>N({...k,[e]:t.target.value})})))),_?Object(m.jsx)(l.a.Fragment,null,Object(m.jsx)(h,null,Object(m.jsx)("div",{className:"confirm-overwrite"},n),Object(m.jsx)("div",{className:"control-label"},Object(d.e)('Type "%s" to confirm',Object(d.e)("OVERWRITE"))),Object(m.jsx)("input",{id:"overwrite",type:"text",onChange:H}))):null)}},4697:function(e,t,a){"use strict";a.d(t,"a",(function(){return s}));var n=a(13);const s={name:Object(n.e)("Data"),tabs:[{name:"Databases",label:Object(n.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(n.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(n.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(n.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},4767:function(e,t,a){"use strict";a.d(t,"a",(function(){return w}));var n=a(25),s=a.n(n),i=(a(0),a(40)),o=a(13),r=a(641),l=a.n(r),c=a(1931),d=a.n(c),u=a(1930),b=a.n(u),g=a(1932),p=a.n(g),m=a(524),j=a.n(m),h=a(359),O=a.n(h),y=a(31),x=a(326),v=a(1);O.a.registerLanguage("sql",l.a),O.a.registerLanguage("markdown",b.a),O.a.registerLanguage("html",d.a),O.a.registerLanguage("json",p.a);const f=i.g.div`
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
`;function w({addDangerToast:e,addSuccessToast:t,children:a,...n}){return Object(v.jsx)(f,null,Object(v.jsx)(y.a.Copy,{tabIndex:0,role:"button",onClick:n=>{var s;n.preventDefault(),n.currentTarget.blur(),s=a,Object(x.a)(s).then(()=>{t&&t(Object(o.e)("SQL Copied!"))}).catch(()=>{e&&e(Object(o.e)("Sorry, your browser does not support copying."))})}}),Object(v.jsx)(O.a,s()({style:j.a},n),a))}},4768:function(e,t,a){"use strict";a.d(t,"a",(function(){return o}));a(41);var n=a(637),s=a.n(n),i=a(0);function o({queries:e,fetchData:t,currentQueryId:a}){const n=s()(e).call(e,e=>e.id===a),[o,r]=Object(i.useState)(n),[l,c]=Object(i.useState)(!1),[d,u]=Object(i.useState)(!1);function b(){c(0===o),u(o===e.length-1)}function g(a){const n=o+(a?-1:1);n>=0&&n<e.length&&(t(e[n].id),r(n),b())}return Object(i.useEffect)(()=>{b()}),{handleKeyPress:function(t){o>=0&&o<e.length&&("ArrowDown"===t.key||"k"===t.key?(t.preventDefault(),g(!1)):"ArrowUp"!==t.key&&"j"!==t.key||(t.preventDefault(),g(!0)))},handleDataChange:g,disablePrevious:l,disableNext:d}}},5077:function(e,t,a){"use strict";a.r(t);a(41);var n=a(35),s=a.n(n),i=a(11),o=a.n(i),r=a(13),l=a(40),c=a(66),d=a(0),u=a.n(d),b=a(111),g=a.n(b),p=a(37),m=a.n(p),j=a(117),h=a(144),O=a(142),y=a(418),x=a(1584),v=a(1585),f=a(720),w=a(4669),S=a(171),k=a(961),N=a(4681),_=a(51),E=a(4697),C=a(326),q=a(42),D=a(4682),$=a(31),T=a(114),M=a(45),I=a(4767),R=a(4768),L=a(1);const B=l.g.div`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
  margin-bottom: 0;
  text-transform: uppercase;
`,H=l.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
  font-size: ${({theme:e})=>e.typography.sizes.m-1}px;
  padding: 4px 0 16px 0;
`,P=Object(l.g)(T.b)`
  .ant-modal-content {
  }

  .ant-modal-body {
    padding: 24px;
  }

  pre {
    font-size: ${({theme:e})=>e.typography.sizes.xs}px;
    font-weight: ${({theme:e})=>e.typography.weights.normal};
    line-height: ${({theme:e})=>e.typography.sizes.l}px;
    height: 375px;
    border: none;
  }
`;var U=Object(O.a)(({fetchData:e,onHide:t,openInSqlLab:a,queries:n,savedQuery:s,show:i,addDangerToast:o,addSuccessToast:l})=>{const{handleKeyPress:c,handleDataChange:d,disablePrevious:u,disableNext:b}=Object(R.a)({queries:n,currentQueryId:s.id,fetchData:e});return Object(L.jsx)("div",{role:"none",onKeyUp:c},Object(L.jsx)(P,{onHide:t,show:i,title:Object(r.e)("Query preview"),footer:[Object(L.jsx)(M.a,{key:"previous-saved-query",disabled:u,onClick:()=>d(!0)},Object(r.e)("Previous")),Object(L.jsx)(M.a,{key:"next-saved-query",disabled:b,onClick:()=>d(!1)},Object(r.e)("Next")),Object(L.jsx)(M.a,{key:"open-in-sql-lab",buttonStyle:"primary",onClick:()=>a(s.id)},Object(r.e)("Open in SQL Lab"))]},Object(L.jsx)(B,null,Object(r.e)("Query name")),Object(L.jsx)(H,null,s.label),Object(L.jsx)(I.a,{language:"sql",addDangerToast:o,addSuccessToast:l},s.sql||"")))});const z=Object(r.e)('The passwords for the databases below are needed in order to import them together with the saved queries. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),A=Object(r.e)("You are importing one or more saved queries that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),Q=l.g.div`
  .count {
    margin-left: 5px;
    color: ${({theme:e})=>e.colors.primary.base};
    text-decoration: underline;
    cursor: pointer;
  }
`,F=l.g.div`
  color: ${({theme:e})=>e.colors.grayscale.dark2};
`;t.default=Object(O.a)((function({addDangerToast:e,addSuccessToast:t,user:a}){const{state:{loading:n,resourceCount:i,resourceCollection:l,bulkSelectEnabled:b},hasPerm:p,fetchData:O,toggleBulkSelect:T,refreshData:M}=Object(y.k)("saved_query",Object(r.e)("Saved queries"),e),[I,R]=Object(d.useState)(null),[B,H]=Object(d.useState)(null),[P,G]=Object(d.useState)(!1),[K,V]=Object(d.useState)([]),[J,W]=Object(d.useState)(!1),X=()=>{G(!0)},Y=p("can_write"),Z=p("can_write"),ee=p("can_read")&&Object(q.c)(q.a.VERSIONED_EXPORT),te=Object(d.useCallback)(t=>{c.a.get({endpoint:`/api/v1/saved_query/${t}`}).then(({json:e={}})=>{H({...e.result})},Object(j.e)(t=>e(Object(r.e)("There was an issue previewing the selected query %s",t))))},[e]),ae={activeChild:"Saved queries",...E.a},ne=[];Z&&ne.push({name:Object(r.e)("Bulk select"),onClick:T,buttonStyle:"secondary"}),ne.push({name:Object(L.jsx)(u.a.Fragment,null,Object(L.jsx)("i",{className:"fa fa-plus"})," ",Object(r.e)("Query")),onClick:()=>{window.open(`${window.location.origin}/superset/sqllab?new=true`)},buttonStyle:"primary"}),Object(q.c)(q.a.VERSIONED_EXPORT)&&ne.push({name:Object(L.jsx)(_.a,{id:"import-tooltip",title:Object(r.e)("Import queries"),placement:"bottomRight"},Object(L.jsx)($.a.Import,null)),buttonStyle:"link",onClick:X,"data-test":"import-button"}),ae.buttons=ne;const se=e=>{window.open(`${window.location.origin}/superset/sqllab?savedQueryId=${e}`)},ie=Object(d.useCallback)(a=>{Object(C.a)(`${window.location.origin}/superset/sqllab?savedQueryId=${a}`).then(()=>{t(Object(r.e)("Link Copied!"))}).catch(()=>{e(Object(r.e)("Sorry, your browser does not support copying."))})},[e,t]),oe=e=>{const t=o()(e).call(e,({id:e})=>e);Object(v.a)("saved_query",t,()=>{W(!1)}),W(!0)},re=[{id:"changed_on_delta_humanized",desc:!0}],le=Object(d.useMemo)(()=>[{accessor:"label",Header:Object(r.e)("Name")},{accessor:"database.database_name",Header:Object(r.e)("Database"),size:"xl"},{accessor:"database",hidden:!0,disableSortBy:!0},{accessor:"schema",Header:Object(r.e)("Schema"),size:"xl"},{Cell:({row:{original:{sql_tables:e=[]}}})=>{const t=o()(e).call(e,e=>e.table),a=(null==t?void 0:t.shift())||"";return t.length?Object(L.jsx)(Q,null,Object(L.jsx)("span",null,a),Object(L.jsx)(h.a,{placement:"right",title:Object(r.e)("TABLES"),trigger:"click",content:Object(L.jsx)(u.a.Fragment,null,o()(t).call(t,e=>Object(L.jsx)(F,{key:e},e)))},Object(L.jsx)("span",{className:"count"},"(+",t.length,")"))):a},accessor:"sql_tables",Header:Object(r.e)("Tables"),size:"xl",disableSortBy:!0},{Cell:({row:{original:{created_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return m()(a).fromNow()},Header:Object(r.e)("Created on"),accessor:"created_on",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>e,Header:Object(r.e)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:e}})=>{var t;const a=s()(t=[{label:"preview-action",tooltip:Object(r.e)("Query preview"),placement:"bottom",icon:"Binoculars",onClick:()=>{te(e.id)}},Y&&{label:"edit-action",tooltip:Object(r.e)("Edit query"),placement:"bottom",icon:"Edit",onClick:()=>se(e.id)},{label:"copy-action",tooltip:Object(r.e)("Copy query URL"),placement:"bottom",icon:"Copy",onClick:()=>ie(e.id)},ee&&{label:"export-action",tooltip:Object(r.e)("Export query"),placement:"bottom",icon:"Share",onClick:()=>oe([e])},Z&&{label:"delete-action",tooltip:Object(r.e)("Delete query"),placement:"bottom",icon:"Trash",onClick:()=>R(e)}]).call(t,e=>!!e);return Object(L.jsx)(N.a,{actions:a})},Header:Object(r.e)("Actions"),id:"actions",disableSortBy:!0}],[Z,Y,ee,ie,te]),ce=Object(d.useMemo)(()=>[{Header:Object(r.e)("Database"),id:"database",input:"select",operator:w.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(j.g)("saved_query","database",Object(j.e)(t=>e(Object(r.e)("An error occurred while fetching dataset datasource values: %s",t)))),paginate:!0},{Header:Object(r.e)("Schema"),id:"schema",input:"select",operator:w.a.equals,unfilteredLabel:"All",fetchSelects:Object(j.f)("saved_query","schema",Object(j.e)(t=>e(Object(r.e)("An error occurred while fetching schema values: %s",t)))),paginate:!0},{Header:Object(r.e)("Search"),id:"label",input:"search",operator:w.a.allText}],[e]);return Object(L.jsx)(u.a.Fragment,null,Object(L.jsx)(f.a,ae),I&&Object(L.jsx)(k.a,{description:Object(r.e)("This action will permanently delete the saved query."),onConfirm:()=>{I&&(({id:a,label:n})=>{c.a.delete({endpoint:`/api/v1/saved_query/${a}`}).then(()=>{M(),R(null),t(Object(r.e)("Deleted: %s",n))},Object(j.e)(t=>e(Object(r.e)("There was an issue deleting %s: %s",n,t))))})(I)},onHide:()=>R(null),open:!0,title:Object(r.e)("Delete Query?")}),B&&Object(L.jsx)(U,{fetchData:te,onHide:()=>H(null),savedQuery:B,queries:l,openInSqlLab:se,show:!0}),Object(L.jsx)(x.a,{title:Object(r.e)("Please confirm"),description:Object(r.e)("Are you sure you want to delete the selected queries?"),onConfirm:a=>{c.a.delete({endpoint:`/api/v1/saved_query/?q=${g.a.encode(o()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{M(),t(e.message)},Object(j.e)(t=>e(Object(r.e)("There was an issue deleting the selected queries: %s",t))))}},e=>{const t=[];return Z&&t.push({key:"delete",name:Object(r.e)("Delete"),onSelect:e,type:"danger"}),ee&&t.push({key:"export",name:Object(r.e)("Export"),type:"primary",onSelect:oe}),Object(L.jsx)(w.b,{className:"saved_query-list-view",columns:le,count:i,data:l,fetchData:O,filters:ce,initialSort:re,loading:n,pageSize:25,bulkActions:t,bulkSelectEnabled:b,disableBulkSelect:T,highlightRowId:null==B?void 0:B.id})}),Object(L.jsx)(D.a,{resourceName:"saved_query",resourceLabel:Object(r.e)("queries"),passwordsNeededMessage:z,confirmOverwriteMessage:A,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{G(!1),M()},show:P,onHide:()=>{G(!1)},passwordFields:K,setPasswordFields:V}),J&&Object(L.jsx)(S.a,null))}))}}]);