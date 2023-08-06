(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{4669:function(e,t,a){"use strict";a.d(t,"a",(function(){return Ue})),a.d(t,"b",(function(){return Ee}));var l,n,o=a(11),i=a.n(o),r=a(26),s=a.n(r),c=a(50),d=a.n(c),g=a(25),u=a.n(g),p=a(40),b=a(13),h=a(0),m=a.n(h),x=a(19),j=a(213);function f(){return(f=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var a=arguments[t];for(var l in a)Object.prototype.hasOwnProperty.call(a,l)&&(e[l]=a[l])}return e}).apply(this,arguments)}function v(e){return h.createElement("svg",f({width:119,height:76,fill:"none",xmlns:"http://www.w3.org/2000/svg"},e),l||(l=h.createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M83.195 1.366L103 24v38a4 4 0 01-4 4H20a4 4 0 01-4-4V24L35.805 1.366A4 4 0 0138.815 0h41.37a4 4 0 013.01 1.366zM101 26v36a2 2 0 01-2 2H20a2 2 0 01-2-2V26h17.25A4.75 4.75 0 0140 30.75a6.75 6.75 0 006.75 6.75h25.5A6.75 6.75 0 0079 30.75 4.75 4.75 0 0183.75 26H101zm-.658-2L81.69 2.683A2 2 0 0080.185 2h-41.37a2 2 0 00-1.505.683L18.657 24H35.25A6.75 6.75 0 0142 30.75a4.75 4.75 0 004.75 4.75h25.5A4.75 4.75 0 0077 30.75 6.75 6.75 0 0183.75 24h16.592z",fill:"#D1D1D1"})),n||(n=h.createElement("path",{d:"M16 53.29C6.074 55.7 0 58.94 0 62.5 0 69.956 26.64 76 59.5 76S119 69.956 119 62.5c0-3.56-6.074-6.799-16-9.21V62a4 4 0 01-4 4H20a4 4 0 01-4-4v-8.71z",fill:"#F2F2F2"})))}a.p;var O=a(5),y=a.n(O),w=a(45),S=a(31),C=a(4822),k=a(447),$=(a(41),a(1));const F=p.g.div`
  ${({theme:e,showThumbnails:t})=>`\n    display: grid;\n    grid-gap: ${12*e.gridUnit}px ${4*e.gridUnit}px;\n    grid-template-columns: repeat(auto-fit, 300px);\n    margin-top: ${-6*e.gridUnit}px;\n    padding: ${t?`${8*e.gridUnit+3}px ${9*e.gridUnit}px`:`${8*e.gridUnit+1}px ${9*e.gridUnit}px`};\n  `}
`,T=p.g.div`
  border: 2px solid transparent;
  &.card-selected {
    border: 2px solid ${({theme:e})=>e.colors.primary.base};
  }
  &.bulk-select {
    cursor: pointer;
  }
`;function R({bulkSelectEnabled:e,loading:t,prepareRow:a,renderCard:l,rows:n,showThumbnails:o}){var r;return l?Object($.jsx)(F,{showThumbnails:o},t&&0===n.length&&i()(r=[...new Array(25)]).call(r,(e,a)=>Object($.jsx)("div",{key:a},l({loading:t}))),n.length>0&&i()(n).call(n,n=>l?(a(n),Object($.jsx)(T,{className:y()({"card-selected":e&&n.isSelected,"bulk-select":e}),key:n.id,onClick:t=>{return a=t,l=n.toggleRowSelected,void(e&&(a.preventDefault(),a.stopPropagation(),l()));var a,l},role:"none"},l({...n.original,loading:t}))):null)):null}var I=a(186),P=a(115),U=a.n(P);const E=p.g.div`
  position: relative;
`,M=p.g.input`
  width: 200px;
  height: ${({theme:e})=>8*e.gridUnit}px;
  background-image: none;
  border: 1px solid ${({theme:e})=>e.colors.secondary.light2};
  border-radius: 4px;
  box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.075);
  padding: 4px 28px;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  &:focus {
    outline: none;
  }
`,_="\n  position: absolute;\n  z-index: 2;\n  display: block;\n  cursor: pointer;\n",z=Object(p.g)(S.a.Search)`
  ${_};
  top: 4px;
  left: 2px;
`,V=Object(p.g)(S.a.CancelX)`
  ${_};
  right: 0px;
  top: 4px;
`;function A({onChange:e,onClear:t,onSubmit:a,placeholder:l="Search",name:n,value:o}){const i=Object(p.i)();return Object($.jsx)(E,null,Object($.jsx)(z,{iconColor:i.colors.grayscale.base,role:"button",onClick:()=>a()}),Object($.jsx)(M,{onKeyDown:e=>{"Enter"===e.key&&a()},onBlur:()=>a(),placeholder:l,onChange:e,value:o,name:n}),o&&Object($.jsx)(V,{role:"button",iconColor:i.colors.grayscale.base,onClick:()=>t()}))}const N=p.g.div`
  display: inline-flex;
  margin-right: 2em;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  align-items: center;
`,B=p.g.label`
  font-weight: bold;
  margin: 0 0.4em 0 0;
`;function L({Header:e,name:t,initialValue:a,onSubmit:l}){const[n,o]=Object(h.useState)(a||""),i=()=>{o(""),l("")};return Object($.jsx)(N,null,Object($.jsx)(A,{placeholder:e,name:t,value:n,onChange:e=>{o(e.currentTarget.value),""===e.currentTarget.value&&i()},onSubmit:()=>{n&&l(U()(n).call(n))},onClear:i}))}var D=a(54),H=a.n(D),W=a(69),q=a(39),G=a.n(q),J=a(474),X=a.n(J),K=a(36),Q=a.n(K),Y=a(35),Z=a.n(Y),ee=a(44),te=a.n(ee),ae=a(156),le=a.n(ae),ne=a(339),oe=a(2238),ie=a(111),re=a.n(ie);const se={encode:e=>void 0===e?void 0:re.a.encode(e),decode:e=>void 0===e||te()(e)?void 0:re.a.decode(e)};class ce extends Error{constructor(...e){super(...e),this.name="ListViewError"}}function de(e,t){return i()(e).call(e,({id:e,urlDisplay:a,operator:l})=>({id:e,urlDisplay:a,operator:l,value:t[a||e]}))}function ge(e,t){var a;const l=[],n={};return s()(a=G()(e)).call(a,t=>{const a={id:t,value:e[t]};n[t]=a,l.push(a)}),s()(t).call(t,e=>{const t=e.urlDisplay||e.id,a=n[t];a&&(a.operator=e.operator,a.id=e.id)}),l}function ue({fetchData:e,columns:t,data:a,count:l,initialPageSize:n,initialFilters:o=[],initialSort:r=[],bulkSelectMode:c=!1,bulkSelectColumnConfig:d,renderCard:g=!1,defaultViewMode:u="card"}){const[p,b]=Object(oe.d)({filters:se,pageIndex:oe.a,sortColumn:oe.c,sortOrder:oe.c,viewMode:oe.c}),m=Object(h.useMemo)(()=>p.sortColumn&&p.sortOrder?[{id:p.sortColumn,desc:"desc"===p.sortOrder}]:r,[p.sortColumn,p.sortOrder]),x={filters:p.filters?ge(p.filters,o):[],pageIndex:p.pageIndex||0,pageSize:n,sortBy:m},[j,f]=Object(h.useState)(p.viewMode||(g?u:"table")),v=Object(h.useMemo)(()=>{const e=i()(t).call(t,e=>({...e,filter:"exact"}));return c?[d,...e]:e},[c,t]),{getTableProps:O,getTableBodyProps:y,headerGroups:w,rows:S,prepareRow:C,canPreviousPage:k,canNextPage:$,pageCount:F,gotoPage:T,setAllFilters:R,selectedFlatRows:I,toggleAllRowsSelected:P,state:{pageIndex:U,pageSize:E,sortBy:M,filters:_}}=Object(ne.useTable)({columns:v,count:l,data:a,disableFilters:!0,disableSortRemove:!0,initialState:x,manualFilters:!0,manualPagination:!0,manualSortBy:!0,autoResetFilters:!1,pageCount:Math.ceil(l/n)},ne.useFilters,ne.useSortBy,ne.usePagination,ne.useRowState,ne.useRowSelect),[z,V]=Object(h.useState)(p.filters&&o.length?de(o,p.filters):[]);Object(h.useEffect)(()=>{o.length&&V(de(o,p.filters?p.filters:{}))},[o]),Object(h.useEffect)(()=>{const t={};s()(z).call(z,e=>{if(void 0!==e.value&&("string"!=typeof e.value||e.value.length>0)){const a=e.urlDisplay||e.id;t[a]=e.value}});const a={filters:G()(t).length?t:void 0,pageIndex:U};M[0]&&(a.sortColumn=M[0].id,a.sortOrder=M[0].desc?"desc":"asc"),g&&(a.viewMode=j);const l=void 0!==p.pageIndex&&a.pageIndex!==p.pageIndex?"push":"replace";b(a,l),e({pageIndex:U,pageSize:E,sortBy:M,filters:_})},[e,U,E,M,_]),Object(h.useEffect)(()=>{le()(x.pageIndex,U)||T(x.pageIndex)},[p]);return{canNextPage:$,canPreviousPage:k,getTableBodyProps:y,getTableProps:O,gotoPage:T,headerGroups:w,pageCount:F,prepareRow:C,rows:S,selectedFlatRows:I,setAllFilters:R,state:{pageIndex:U,pageSize:E,sortBy:M,filters:_,internalFilters:z,viewMode:j},toggleAllRowsSelected:P,applyFilterValue:(e,t)=>{V(a=>{if(a[e].value===t)return a;const l={...a[e],value:t},n=function(e,t,a){const l=H()(e).call(e,(e,a)=>t===a);return[...Q()(e).call(e,0,t),{...l,...a},...Q()(e).call(e,t+1)]}(a,e,l);var o,r,s;return R((o=n,X()(r=i()(s=Z()(o).call(o,e=>!(void 0===e.value||te()(e.value)&&!e.value.length))).call(s,({value:e,operator:t,id:a})=>"between"===t&&te()(e)?[{value:e[0],operator:"gt",id:a},{value:e[1],operator:"lt",id:a}]:{value:e,operator:t,id:a})).call(r))),T(0),n})},setViewMode:f}}const pe={container:(e,{getValue:t})=>({...e,minWidth:`${Math.min(12,Math.max(5,3+t()[0].label.length/2))}em`}),control:e=>({...e,borderWidth:0,boxShadow:"none",cursor:"pointer",backgroundColor:"transparent"})};var be=Object(I.e)((function({Header:e,emptyLabel:t="None",fetchSelects:a,initialValue:l,onSelect:n,paginate:o=!1,selects:i=[],theme:r}){const s={spacing:{baseUnit:2,fontSize:r.typography.sizes.s,minWidth:"5em"}},c={label:t,value:"CLEAR_SELECT_FILTER_VALUE"},d=[c,...i];let g=c;if(!a){const e=H()(d).call(d,e=>e.value===l);e&&(g=e)}const[u,p]=Object(h.useState)(g),b=e=>{null!==e&&(n("CLEAR_SELECT_FILTER_VALUE"===e.value?void 0:e.value),p(e))};return Object($.jsx)(N,null,Object($.jsx)(B,null,e,":"),a?Object($.jsx)(W.g,{defaultOptions:!0,themeConfig:s,stylesConfig:pe,value:u,onChange:b,loadOptions:async(e,t,{page:n})=>{let i=e||n>0?[]:[c],r=o;if(a){const t=await a(e,n);t.length||(r=!1),i=[...i,...t];const o=H()(i).call(i,e=>e.value===l);o&&p(o)}return{options:i,hasMore:r,additional:{page:n+1}}},placeholder:t,clearable:!1,additional:{page:0}}):Object($.jsx)(W.h,{themeConfig:s,stylesConfig:pe,value:u,options:d,onChange:b,clearable:!1}))})),he=a(37),me=a.n(he),xe=a(706);const je=Object(p.g)(xe.b)`
  padding: 0 11px;
  transform: translateX(-7px);
`,fe=Object(p.g)(N)`
  margin-right: 1em;
`;function ve({Header:e,initialValue:t,onSubmit:a}){const[l,n]=Object(h.useState)(null!=t?t:null),o=Object(h.useMemo)(()=>!l||te()(l)&&!l.length?null:[me()(l[0]),me()(l[1])],[l]);return Object($.jsx)(fe,null,Object($.jsx)(B,null,e,":"),Object($.jsx)(je,{showTime:!0,bordered:!1,value:o,onChange:e=>{var t,l,o,i;if(!e)return n(null),void a([]);const r=[null!=(t=null==(l=e[0])?void 0:l.valueOf())?t:0,null!=(o=null==(i=e[1])?void 0:i.valueOf())?o:0];n(r),a(r)}}))}const Oe=p.g.div`
  display: inline-block;
`;var ye=Object(I.e)((function({filters:e,internalFilters:t=[],updateFilterValue:a}){return Object($.jsx)(Oe,null,i()(e).call(e,({Header:e,fetchSelects:l,id:n,input:o,paginate:i,selects:r,unfilteredLabel:s},c)=>{const d=t[c]&&t[c].value;return"select"===o?Object($.jsx)(be,{Header:e,emptyLabel:s,fetchSelects:l,initialValue:d,key:n,name:n,onSelect:e=>a(c,e),paginate:i,selects:r}):"search"===o&&"string"==typeof e?Object($.jsx)(L,{Header:e,initialValue:d,key:n,name:n,onSubmit:e=>a(c,e)}):"datetime_range"===o?Object($.jsx)(ve,{Header:e,initialValue:d,key:n,name:n,onSubmit:e=>a(c,e)}):null}))}));const we=p.g.label`
  font-weight: bold;
  line-height: 27px;
  margin: 0 0.4em 0 0;
`,Se=p.g.div`
  display: inline-flex;
  font-size: ${({theme:e})=>e.typography.sizes.s}px;
  padding-top: ${({theme:e})=>e.gridUnit}px;
  text-align: left;
`;const Ce=Object(I.e)((function({onChange:e,options:t,selectStyles:a,theme:l,value:n}){const o={spacing:{baseUnit:1,fontSize:l.typography.sizes.s,minWidth:"5em"}};return Object($.jsx)(W.h,{clearable:!1,onChange:e,options:t,stylesConfig:a,themeConfig:o,value:n})})),ke=({initialSort:e,onChange:t,options:a,pageIndex:l,pageSize:n})=>{const o=e&&H()(a).call(a,({id:t})=>t===e[0].id),[i,r]=Object(h.useState)(o||a[0]);return Object($.jsx)(Se,null,Object($.jsx)(we,null,Object(b.e)("Sort:")),Object($.jsx)(Ce,{onChange:e=>(e=>{r(e);const a=[{id:e.id,desc:e.desc}];t({pageIndex:l,pageSize:n,sortBy:a,filters:[]})})(e),options:a,selectStyles:pe,value:i}))},$e=p.g.div`
  text-align: center;

  .superset-list-view {
    text-align: left;
    border-radius: 4px 0;
    margin: 0 ${({theme:e})=>4*e.gridUnit}px;

    .header {
      display: flex;
      padding-bottom: ${({theme:e})=>4*e.gridUnit}px;

      .header-left {
        display: flex;
        flex: 5;
      }
      .header-right {
        flex: 1;
        text-align: right;
      }
    }

    .body.empty table {
      margin-bottom: 0;
    }

    .body {
      overflow-x: auto;
    }

    .ant-empty {
      .ant-empty-image {
        height: auto;
      }
    }
  }

  .pagination-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: ${({theme:e})=>4*e.gridUnit}px;
  }

  .row-count-container {
    margin-top: ${({theme:e})=>2*e.gridUnit}px;
    color: ${({theme:e})=>e.colors.grayscale.base};
  }
`,Fe=Object(p.g)(j.a)`
  border-radius: 0;
  margin-bottom: 0;
  color: #3d3d3d;
  background-color: ${({theme:e})=>e.colors.primary.light4};

  .selectedCopy {
    display: inline-block;
    padding: ${({theme:e})=>2*e.gridUnit}px 0;
  }

  .deselect-all {
    color: #1985a0;
    margin-left: ${({theme:e})=>4*e.gridUnit}px;
  }

  .divider {
    margin: ${({theme:{gridUnit:e}})=>`${2*-e}px 0 ${2*-e}px ${4*e}px`};
    width: 1px;
    height: ${({theme:e})=>8*e.gridUnit}px;
    box-shadow: inset -1px 0px 0px #dadada;
    display: inline-flex;
    vertical-align: middle;
    position: relative;
  }

  .ant-alert-close-icon {
    margin-top: ${({theme:e})=>1.5*e.gridUnit}px;
  }
`,Te={Cell:({row:e})=>Object($.jsx)(C.a,u()({},e.getToggleRowSelectedProps(),{id:e.id})),Header:({getToggleAllRowsSelectedProps:e})=>Object($.jsx)(C.a,u()({},e(),{id:"header-toggle-all"})),id:"selection",size:"sm"},Re=p.g.div`
  padding-right: ${({theme:e})=>4*e.gridUnit}px;
  display: inline-block;

  .toggle-button {
    display: inline-block;
    border-radius: ${({theme:e})=>e.gridUnit/2}px;
    padding: ${({theme:e})=>e.gridUnit}px;
    padding-bottom: ${({theme:e})=>.5*e.gridUnit}px;

    &:first-of-type {
      margin-right: ${({theme:e})=>2*e.gridUnit}px;
    }
  }

  .active {
    background-color: ${({theme:e})=>e.colors.grayscale.base};
    svg {
      color: ${({theme:e})=>e.colors.grayscale.light5};
    }
  }
`,Ie=p.g.div`
  padding: ${({theme:e})=>40*e.gridUnit}px 0;

  &.table {
    background: ${({theme:e})=>e.colors.grayscale.light5};
  }
`,Pe=({mode:e,setMode:t})=>Object($.jsx)(Re,null,Object($.jsx)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("card")},className:y()("toggle-button",{active:"card"===e})},Object($.jsx)(S.a.CardView,null)),Object($.jsx)("div",{role:"button",tabIndex:0,onClick:e=>{e.currentTarget.blur(),t("table")},className:y()("toggle-button",{active:"table"===e})},Object($.jsx)(S.a.ListView,null)));var Ue,Ee=function({columns:e,data:t,count:a,pageSize:l,fetchData:n,loading:o,initialSort:r=[],className:c="",filters:g=[],bulkActions:u=[],bulkSelectEnabled:p=!1,disableBulkSelect:j=(()=>{}),renderBulkSelectCopy:f=(e=>Object(b.e)("%s Selected",e.length)),renderCard:O,showThumbnails:y,cardSortSelectOptions:S,defaultViewMode:C="card",highlightRowId:F,emptyState:T={}}){const{getTableProps:I,getTableBodyProps:P,headerGroups:U,rows:E,prepareRow:M,pageCount:_=1,gotoPage:z,applyFilterValue:V,selectedFlatRows:A,toggleAllRowsSelected:N,setViewMode:B,state:{pageIndex:L,pageSize:D,internalFilters:H,viewMode:W}}=ue({bulkSelectColumnConfig:Te,bulkSelectMode:p&&Boolean(u.length),columns:e,count:a,data:t,fetchData:n,initialPageSize:l,initialSort:r,initialFilters:g,renderCard:Boolean(O),defaultViewMode:C}),q=Boolean(g.length);if(q){const t=d()(e).call(e,(e,t)=>({...e,[t.id||t.accessor]:!0}),{});s()(g).call(g,e=>{if(!t[e.id])throw new ce(`Invalid filter config, ${e.id} is not present in columns`)})}const G=Boolean(O);return Object(h.useEffect)(()=>{p||N(!1)},[p,N]),Object($.jsx)($e,null,Object($.jsx)("div",{className:`superset-list-view ${c}`},Object($.jsx)("div",{className:"header"},Object($.jsx)("div",{className:"header-left"},G&&Object($.jsx)(Pe,{mode:W,setMode:B}),q&&Object($.jsx)(ye,{filters:g,internalFilters:H,updateFilterValue:V})),Object($.jsx)("div",{className:"header-right"},"card"===W&&S&&Object($.jsx)(ke,{initialSort:r,onChange:n,options:S,pageIndex:L,pageSize:D}))),Object($.jsx)("div",{className:`body ${0===E.length?"empty":""}`},p&&Object($.jsx)(Fe,{type:"info",closable:!0,showIcon:!1,onClose:j,message:Object($.jsx)(m.a.Fragment,null,Object($.jsx)("div",{className:"selectedCopy"},f(A)),Boolean(A.length)&&Object($.jsx)(m.a.Fragment,null,Object($.jsx)("span",{role:"button",tabIndex:0,className:"deselect-all",onClick:()=>N(!1)},Object(b.e)("Deselect all")),Object($.jsx)("div",{className:"divider"}),i()(u).call(u,e=>Object($.jsx)(w.a,{key:e.key,buttonStyle:e.type,cta:!0,onClick:()=>e.onSelect(i()(A).call(A,e=>e.original))},e.name))))}),"card"===W&&Object($.jsx)(R,{bulkSelectEnabled:p,prepareRow:M,renderCard:O,rows:E,loading:o,showThumbnails:y}),"table"===W&&Object($.jsx)(k.b,{getTableProps:I,getTableBodyProps:P,prepareRow:M,headerGroups:U,rows:E,columns:e,loading:o,highlightRowId:F}),!o&&0===E.length&&Object($.jsx)(Ie,{className:W},Object($.jsx)(x.k,{image:Object($.jsx)(v,null),description:T.message||Object(b.e)("No Data")},T.slot||null)))),E.length>0&&Object($.jsx)("div",{className:"pagination-container"},Object($.jsx)(k.a,{totalPages:_||0,currentPage:_?L+1:0,onChange:e=>z(e-1),hideFirstAndLastPageLinks:!0}),Object($.jsx)("div",{className:"row-count-container"},!o&&Object(b.e)("%s-%s of %s",D*L+(E.length&&1),D*L+E.length,a))))};!function(e){e.startsWith="sw",e.endsWith="ew",e.contains="ct",e.equals="eq",e.notStartsWith="nsw",e.notEndsWith="new",e.notContains="nct",e.notEquals="neq",e.greaterThan="gt",e.lessThan="lt",e.relationManyMany="rel_m_m",e.relationOneMany="rel_o_m",e.titleOrSlug="title_or_slug",e.nameOrDescription="name_or_description",e.allText="all_text",e.chartAllText="chart_all_text",e.datasetIsNullOrEmpty="dataset_is_null_or_empty",e.between="between",e.dashboardIsFav="dashboard_is_favorite",e.chartIsFav="chart_is_favorite"}(Ue||(Ue={}))},4822:function(e,t,a){"use strict";var l=a(0),n=a.n(l),o=a(40),i=a(31),r=a(1);const s=o.g.label`
  cursor: pointer;
  display: inline-block;
  margin-bottom: 0;
`,c=Object(o.g)(i.a.CheckboxHalf)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,d=Object(o.g)(i.a.CheckboxOff)`
  color: ${({theme:e})=>e.colors.grayscale.base};
  cursor: pointer;
`,g=Object(o.g)(i.a.CheckboxOn)`
  color: ${({theme:e})=>e.colors.primary.base};
  cursor: pointer;
`,u=o.g.input`
  &[type='checkbox'] {
    cursor: pointer;
    opacity: 0;
    position: absolute;
    left: 3px;
    margin: 0;
    top: 4px;
  }
`,p=o.g.div`
  cursor: pointer;
  display: inline-block;
  position: relative;
`,b=n.a.forwardRef(({indeterminate:e,id:t,checked:a,onChange:l,title:o="",labelText:i=""},b)=>{const h=n.a.useRef(),m=b||h;return n.a.useEffect(()=>{m.current.indeterminate=e},[m,e]),Object(r.jsx)(n.a.Fragment,null,Object(r.jsx)(p,null,e&&Object(r.jsx)(c,null),!e&&a&&Object(r.jsx)(g,null),!e&&!a&&Object(r.jsx)(d,null),Object(r.jsx)(u,{name:t,id:t,type:"checkbox",ref:m,checked:a,onChange:l})),Object(r.jsx)(s,{title:o,htmlFor:t},i))});t.a=b}}]);