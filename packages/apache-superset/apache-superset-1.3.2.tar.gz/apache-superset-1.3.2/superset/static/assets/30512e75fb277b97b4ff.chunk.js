(window.webpackJsonp=window.webpackJsonp||[]).push([[18],{1588:function(e,t,a){"use strict";var n=a(0),s=a.n(n),l=a(51),c=a(31),o=a(1);t.a=({onClick:e,tooltipContent:t})=>{const a=s.a.forwardRef((e,t)=>Object(o.jsx)(c.a.Refresh,e));return Object(o.jsx)(l.a,{title:t},Object(o.jsx)(a,{role:"button",onClick:e,css:e=>({cursor:"pointer",color:e.colors.grayscale.base,"&:hover":{color:e.colors.primary.base}})}))}},1938:function(e,t,a){"use strict";var n=a(0),s=a.n(n),l=a(13),c=a(40),o=a(31),i=a(51),r=a(1);t.a=function({certifiedBy:e,details:t,size:a=24}){return Object(r.jsx)(i.a,{id:"certified-details-tooltip",title:Object(r.jsx)(s.a.Fragment,null,e&&Object(r.jsx)("div",null,Object(r.jsx)("strong",null,Object(l.e)("Certified by %s",e))),Object(r.jsx)("div",null,t))},Object(r.jsx)(o.a.Certified,{iconColor:c.h.colors.primary.base,height:a,width:a}))}},1946:function(e,t,a){"use strict";a(41);var n=a(55),s=a.n(n),l=a(11),c=a.n(l),o=a(0),i=a(40),r=a(66),d=a(13),b=a(69),u=a(74),j=a(1947),m=a(1588),h=a(1938),p=a(726),f=a(1);const x=i.g.p`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin: 20px 0 10px 0;
  text-transform: uppercase;
`,g=i.g.div`
  .fa-refresh {
    padding-left: 9px;
  }

  .refresh-col {
    display: flex;
    align-items: center;
    width: 30px;
    margin-left: ${({theme:e})=>e.gridUnit}px;
  }

  .section {
    padding-bottom: 5px;
    display: flex;
    flex-direction: row;
  }

  .select {
    flex-grow: 1;
  }

  .divider {
    border-bottom: 1px solid ${({theme:e})=>e.colors.secondary.light5};
    margin: 15px 0;
  }

  .table-length {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`,O=i.g.span`
  align-items: center;
  display: flex;
  white-space: nowrap;

  svg,
  small {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`;t.a=({database:e,dbId:t,formMode:a=!1,getDbList:n,handleError:l,isDatabaseSelectEnabled:i=!0,onUpdate:v,onDbChange:y,onSchemaChange:w,onSchemasLoad:C,onTableChange:S,onTablesLoad:$,readOnly:N=!1,schema:I,sqlLabMode:_=!0,tableName:L,tableNameSticky:R=!0})=>{const[D,E]=Object(o.useState)(I),[k,z]=Object(o.useState)(L),[U,q]=Object(o.useState)(!1),[M,T]=Object(o.useState)([]);function A(e,a,n=!1,o="undefined"){const i=a||D,b=e||t;if(b&&i){const e=encodeURIComponent(i),t=encodeURIComponent(o);q(!0),T([]);const a=encodeURI(`/superset/tables/${b}/${e}/${t}/${!!n}/`);return r.a.get({endpoint:a}).then(({json:e})=>{var t;const a=c()(t=e.options).call(t,e=>({value:e.value,schema:e.schema,label:e.label,title:e.title,type:e.type,extra:null==e?void 0:e.extra}));q(!1),T(a),$&&$(e.options)}).catch(()=>{q(!1),T([]),l(Object(d.e)("Error while fetching table list"))})}return q(!1),T([]),s.a.resolve()}function B({dbId:e,schema:t,tableName:a}){z(a),E(t),v&&v({dbId:e,schema:t,tableName:a})}function F(e="undefined"){if(!t||!e){const e=[];return s.a.resolve({options:e})}const a=encodeURIComponent(I||""),n=encodeURIComponent(e);return r.a.get({endpoint:encodeURI(`/superset/tables/${t}/${a}/${n}`)}).then(({json:e})=>{var t;return{options:c()(t=e.options).call(t,e=>({value:e.value,schema:e.schema,label:e.label,title:e.title,type:e.type}))}})}function J(e){if(!e)return void z("");const a=e.schema,n=e.value;R&&B({dbId:t,schema:a,tableName:n}),S&&S(n,a)}function K(e){var t,a;return Object(f.jsx)(O,{title:e.label},Object(f.jsx)("small",{className:"text-muted"},Object(f.jsx)("i",{className:`fa fa-${"view"===e.type?"eye":"table"}`})),(null==(t=e.extra)?void 0:t.certification)&&Object(f.jsx)(h.a,{certifiedBy:e.extra.certification.certified_by,details:e.extra.certification.details,size:20}),(null==(a=e.extra)?void 0:a.warning_markdown)&&Object(f.jsx)(p.a,{warningMarkdown:e.extra.warning_markdown,size:20}),e.label)}return Object(o.useEffect)(()=>{t&&I&&A()},[t,I]),Object(f.jsx)(g,null,Object(f.jsx)(j.a,{dbId:t,formMode:a,getDbList:n,getTableList:A,handleError:l,onUpdate:B,onDbChange:N?void 0:y,onSchemaChange:N?void 0:w,onSchemasLoad:C,schema:D,sqlLabMode:_,isDatabaseSelectEnabled:i&&!N,readOnly:N}),!a&&Object(f.jsx)("div",{className:"divider"}),_&&Object(f.jsx)("div",{className:"section"},Object(f.jsx)(u.c,null,Object(d.e)("See table schema")," ",I&&Object(f.jsx)("small",{className:"table-length"},M.length," in ",I))),a&&Object(f.jsx)(x,null,Object(d.e)("Table")),function(){const n=M;let s=null;if(D&&!a)s=Object(f.jsx)(b.h,{name:"select-table",isLoading:U,ignoreAccents:!1,placeholder:Object(d.e)("Select table or type table name"),autosize:!1,onChange:J,options:n,value:k,optionRenderer:K,valueRenderer:K,isDisabled:N});else if(a)s=Object(f.jsx)(b.c,{name:"select-table",isLoading:U,ignoreAccents:!1,placeholder:Object(d.e)("Select table or type table name"),autosize:!1,onChange:J,options:n,value:k,optionRenderer:K});else{let t,a=!1;e&&e.allow_multi_schema_metadata_fetch?t=Object(d.e)("Type to search ..."):(t=Object(d.e)("Select table "),a=!0),s=Object(f.jsx)(b.b,{name:"async-select-table",placeholder:t,isDisabled:a,autosize:!1,onChange:J,value:k,loadOptions:F,optionRenderer:K})}return function(e,t){return Object(f.jsx)("div",{className:"section"},Object(f.jsx)("span",{className:"select"},e),Object(f.jsx)("span",{className:"refresh-col"},t))}(s,!a&&!N&&Object(f.jsx)(m.a,{onClick:()=>function(e,a=!1){const n=e?e.value:null;w&&w(n),B({dbId:t,schema:n,tableName:void 0}),A(t,D,a)}({value:I},!0),tooltipContent:Object(d.e)("Force refresh table list")}))}())}},1947:function(e,t,a){"use strict";a.d(t,"a",(function(){return w}));a(41);var n=a(35),s=a.n(n),l=a(55),c=a.n(l),o=a(11),i=a.n(o),r=a(0),d=a(40),b=a(66),u=a(13),j=a(111),m=a.n(j),h=a(69),p=a(123),f=a(1588),x=a(596),g=a(1);const O=d.g.p`
  color: ${({theme:e})=>e.colors.secondary.light2};
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  margin: 20px 0 10px 0;
  text-transform: uppercase;
`,v=d.g.div`
  .fa-refresh {
    padding-left: 9px;
  }

  .refresh-col {
    display: flex;
    align-items: center;
    width: 30px;
    margin-left: ${({theme:e})=>e.gridUnit}px;
  }

  .section {
    padding-bottom: 5px;
    display: flex;
    flex-direction: row;
  }

  .select {
    flex-grow: 1;
  }
`,y=d.g.span`
  display: inline-flex;
  align-items: center;
`;function w({dbId:e,formMode:t=!1,getDbList:a,getTableList:n,handleError:l,isDatabaseSelectEnabled:o=!0,onUpdate:d,onDbChange:j,onSchemaChange:w,onSchemasLoad:C,readOnly:S=!1,schema:$,sqlLabMode:N=!1}){const[I,_]=Object(r.useState)(e),[L,R]=Object(r.useState)($),[D,E]=Object(r.useState)(!1),[k,z]=Object(r.useState)([]);function U(t,a=!1){const n=t||e;if(n){E(!0);const e=`/api/v1/database/${n}/schemas/?q=${m.a.encode({force:Boolean(a)})}`;return b.a.get({endpoint:e}).then(({json:e})=>{var t;const a=i()(t=e.result).call(t,e=>({value:e,label:e,title:e}));z(a),E(!1),C&&C(a)}).catch(()=>{z([]),E(!1),l(Object(u.e)("Error while fetching schema list"))})}return c.a.resolve()}function q({dbId:e,schema:t}){_(e),R(t),d&&d({dbId:e,schema:t,tableName:void 0})}function M(e){var t;return a&&a(e.result),0===e.result.length&&l(Object(u.e)("It seems you don't have access to any database")),i()(t=e.result).call(t,e=>({...e,label:`${e.backend} ${e.database_name}`}))}function T(e,t=!1){const a=e?e.id:null;z([]),w&&w(null),j&&j(e),U(a,t),q({dbId:a,schema:void 0})}function A(e){return Object(g.jsx)(y,{title:e.database_name},Object(g.jsx)(p.a,{type:"default"},e.backend)," ",e.database_name)}function B(e,t){return Object(g.jsx)("div",{className:"section"},Object(g.jsx)("span",{className:"select"},e),Object(g.jsx)("span",{className:"refresh-col"},t))}return Object(r.useEffect)(()=>{I&&U(I)},[I]),Object(g.jsx)(v,null,t&&Object(g.jsx)(O,null,Object(u.e)("datasource")),function(){const e=m.a.encode({order_columns:"database_name",order_direction:"asc",page:0,page_size:-1,...t||!N?{}:{filters:[{col:"expose_in_sqllab",opr:"eq",value:!0}]}});return B(Object(g.jsx)(x.a,{dataEndpoint:`/api/v1/database/?q=${e}`,onChange:e=>T(e),onAsyncError:()=>l(Object(u.e)("Error while fetching database list")),clearable:!1,value:I,valueKey:"id",valueRenderer:e=>Object(g.jsx)("div",null,Object(g.jsx)("span",{className:"text-muted m-r-5"},Object(u.e)("Database:")),A(e)),optionRenderer:A,mutator:M,placeholder:Object(u.e)("Select a database"),autoSelect:!0,isDisabled:!o||S}),null)}(),t&&Object(g.jsx)(O,null,Object(u.e)("schema")),function(){const a=s()(k).call(k,({value:e})=>L===e),l=!t&&!S&&Object(g.jsx)(f.a,{onClick:()=>T({id:e},!0),tooltipContent:Object(u.e)("Force refresh schema list")});return B(Object(g.jsx)(h.h,{name:"select-schema",placeholder:Object(u.e)("Select a schema (%s)",k.length),options:k,value:a,valueRenderer:e=>Object(g.jsx)("div",null,Object(g.jsx)("span",{className:"text-muted"},Object(u.e)("Schema:"))," ",e.label),isLoading:D,autosize:!1,onChange:e=>function(e,t=!1){const a=e?e.value:null;w&&w(a),R(a),q({dbId:I,schema:a}),n&&n(I,a,t)}(e),isDisabled:S}),l)}())}}}]);