(window.webpackJsonp=window.webpackJsonp||[]).push([[31],{4682:function(e,t,a){"use strict";a(41);var s=a(11),l=a.n(s),c=a(35),n=a.n(c),r=a(0),i=a.n(r),o=a(40),d=a(13),b=a(45),u=a(114),j=a(19),O=a(418),p=a(1);const m=o.g.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,h=o.g.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:s,addDangerToast:c,addSuccessToast:o,onModelImport:g,show:x,onHide:y,passwordFields:w=[],setPasswordFields:f=(()=>{})})=>{const[v,S]=Object(r.useState)(!0),[k,_]=Object(r.useState)({}),[C,D]=Object(r.useState)(!1),[N,H]=Object(r.useState)(!1),[$,T]=Object(r.useState)([]),[A,E]=Object(r.useState)(!1),B=()=>{T([]),f([]),_({}),D(!1),H(!1),E(!1)},{state:{alreadyExists:I,passwordsNeeded:M},importResource:R}=Object(O.j)(e,t,e=>{B(),c(e)});Object(r.useEffect)(()=>{f(M),M.length>0&&E(!1)},[M,f]),Object(r.useEffect)(()=>{D(I.length>0),I.length>0&&E(!1)},[I,D]);const z=e=>{var t,a;const s=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";H(s.toUpperCase()===Object(d.e)("OVERWRITE"))};return v&&x&&S(!1),Object(p.jsx)(u.b,{name:"model",className:"import-model-modal",disablePrimaryButton:0===$.length||C&&!N||A,onHandledPrimaryAction:()=>{var e;(null==(e=$[0])?void 0:e.originFileObj)instanceof File&&(E(!0),R($[0].originFileObj,k,N).then(e=>{e&&(o(Object(d.e)("The import was successful")),B(),g())}))},onHide:()=>{S(!0),y(),B()},primaryButtonName:C?Object(d.e)("Overwrite"):Object(d.e)("Import"),primaryButtonType:C?"danger":"primary",width:"750px",show:x,title:Object(p.jsx)("h4",null,Object(d.e)("Import %s",t))},Object(p.jsx)(h,null,Object(p.jsx)(j.F,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:$,onChange:e=>{T([{...e.file,status:"done"}])},onRemove:e=>(T(n()($).call($,t=>t.uid!==e.uid)),!1),customRequest:()=>{}},Object(p.jsx)(b.a,{loading:A},"Select file"))),0===w.length?null:Object(p.jsx)(i.a.Fragment,null,Object(p.jsx)("h5",null,"Database passwords"),Object(p.jsx)(m,null,a),l()(w).call(w,e=>Object(p.jsx)(h,{key:`password-for-${e}`},Object(p.jsx)("div",{className:"control-label"},e,Object(p.jsx)("span",{className:"required"},"*")),Object(p.jsx)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:k[e],onChange:t=>_({...k,[e]:t.target.value})})))),C?Object(p.jsx)(i.a.Fragment,null,Object(p.jsx)(h,null,Object(p.jsx)("div",{className:"confirm-overwrite"},s),Object(p.jsx)("div",{className:"control-label"},Object(d.e)('Type "%s" to confirm',Object(d.e)("OVERWRITE"))),Object(p.jsx)("input",{id:"overwrite",type:"text",onChange:z}))):null)}},4697:function(e,t,a){"use strict";a.d(t,"a",(function(){return l}));var s=a(13);const l={name:Object(s.e)("Data"),tabs:[{name:"Databases",label:Object(s.e)("Databases"),url:"/databaseview/list/",usesRouter:!0},{name:"Datasets",label:Object(s.e)("Datasets"),url:"/tablemodelview/list/",usesRouter:!0},{name:"Saved queries",label:Object(s.e)("Saved queries"),url:"/savedqueryview/list/",usesRouter:!0},{name:"Query history",label:Object(s.e)("Query history"),url:"/superset/sqllab/history/",usesRouter:!0}]}},5075:function(e,t,a){"use strict";a.r(t);a(41);var s=a(50),l=a.n(s),c=a(36),n=a.n(c),r=a(11),i=a.n(r),o=a(40),d=a(13),b=a(66),u=a(0),j=a.n(u),O=a(111),p=a.n(O),m=a(117),h=a(418),g=a(1584),x=a(1304),y=a(961),w=a(1585),f=a(4669),v=a(171),S=a(720),k=a(4697),_=a(142),C=a(51),D=a(31),N=a(672),H=a(1938),$=a(4682),T=a(42),A=a(726),E=a(659),B=a.n(E),I=a(330),M=a.n(I),R=a(114),z=a(1946),F=a(1);const P=o.g.div`
  padding-bottom: 340px;
  width: 65%;
`;var U=Object(_.a)(({addDangerToast:e,addSuccessToast:t,onDatasetAdd:a,onHide:s,show:l})=>{const[c,n]=Object(u.useState)(""),[r,i]=Object(u.useState)(""),[o,b]=Object(u.useState)(0),[j,O]=Object(u.useState)(!0),{createResource:p}=Object(h.l)("dataset",Object(d.e)("dataset"),e);return Object(F.jsx)(R.b,{disablePrimaryButton:j,onHandledPrimaryAction:()=>{const e={database:o,...c?{schema:c}:{},table_name:r};p(e).then(e=>{e&&(a&&a({id:e.id,...e}),t(Object(d.e)("The dataset has been saved")),s())})},onHide:s,primaryButtonName:Object(d.e)("Add"),show:l,title:Object(d.e)("Add dataset")},Object(F.jsx)(P,null,Object(F.jsx)(z.a,{clearable:!1,dbId:o,formMode:!0,handleError:e,onUpdate:({dbId:e,schema:t,tableName:a})=>{b(e),O(B()(e)||M()(a)),n(t),i(a)},schema:c,tableName:r})))}),q=a(629);const V=o.g.div`
  align-items: center;
  display: flex;

  svg {
    margin-right: ${({theme:e})=>e.gridUnit}px;
  }
`,L=o.g.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(_.a)(({addDangerToast:e,addSuccessToast:t,user:a})=>{const{state:{loading:s,resourceCount:c,resourceCollection:r,bulkSelectEnabled:o},hasPerm:O,fetchData:_,toggleBulkSelect:E,refreshData:B}=Object(h.k)("dataset",Object(d.e)("dataset"),e),[I,M]=Object(u.useState)(!1),[R,z]=Object(u.useState)(null),[P,J]=Object(u.useState)(null),[Q,W]=Object(u.useState)(!1),[X,G]=Object(u.useState)([]),[K,Y]=Object(u.useState)(!1),Z=()=>{W(!0)},ee=O("can_write"),te=O("can_write"),ae=O("can_write"),se=O("can_read"),le=q.d,ce=Object(u.useCallback)(({id:t})=>{b.a.get({endpoint:`/api/v1/dataset/${t}`}).then(({json:e={}})=>{var t;const a=i()(t=e.result.owners).call(t,e=>e.id);J({...e.result,owners:a})}).catch(()=>{e(Object(d.e)("An error occurred while fetching dataset related data"))})},[e]),ne=Object(u.useMemo)(()=>[{Cell:({row:{original:{kind:e}}})=>"physical"===e?Object(F.jsx)(C.a,{id:"physical-dataset-tooltip",title:Object(d.e)("Physical dataset")},Object(F.jsx)(D.a.DatasetPhysical,null)):Object(F.jsx)(C.a,{id:"virtual-dataset-tooltip",title:Object(d.e)("Virtual dataset")},Object(F.jsx)(D.a.DatasetVirtual,null)),accessor:"kind_icon",disableSortBy:!0,size:"xs"},{Cell:({row:{original:{extra:e,table_name:t,explore_url:a}}})=>{const s=Object(F.jsx)("a",{href:a},t);try{const t=JSON.parse(e);return Object(F.jsx)(V,null,(null==t?void 0:t.certification)&&Object(F.jsx)(H.a,{certifiedBy:t.certification.certified_by,details:t.certification.details}),(null==t?void 0:t.warning_markdown)&&Object(F.jsx)(A.a,{warningMarkdown:t.warning_markdown}),s)}catch{return s}},Header:Object(d.e)("Name"),accessor:"table_name"},{Cell:({row:{original:{kind:e}}})=>{var t;return(null==(t=e[0])?void 0:t.toUpperCase())+n()(e).call(e,1)},Header:Object(d.e)("Type"),accessor:"kind",disableSortBy:!0,size:"md"},{Header:Object(d.e)("Database"),accessor:"database.database_name",size:"lg"},{Header:Object(d.e)("Schema"),accessor:"schema",size:"lg"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>Object(F.jsx)("span",{className:"no-wrap"},e),Header:Object(d.e)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:{changed_by_name:e}}})=>e,Header:Object(d.e)("Modified by"),accessor:"changed_by.first_name",size:"xl"},{accessor:"database",disableSortBy:!0,hidden:!0},{Cell:({row:{original:{owners:e=[]}}})=>Object(F.jsx)(N.a,{users:e}),Header:Object(d.e)("Owners"),id:"owners",disableSortBy:!0,size:"lg"},{accessor:"sql",hidden:!0,disableSortBy:!0},{Cell:({row:{original:e}})=>ee||te||se?Object(F.jsx)(L,{className:"actions"},te&&Object(F.jsx)(C.a,{id:"delete-action-tooltip",title:Object(d.e)("Delete"),placement:"bottom"},Object(F.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>{return t=e,b.a.get({endpoint:`/api/v1/dataset/${t.id}/related_objects`}).then(({json:e={}})=>{z({...t,chart_count:e.charts.count,dashboard_count:e.dashboards.count})}).catch(Object(m.e)(e=>Object(d.e)("An error occurred while fetching dataset related data: %s",e)));var t}},Object(F.jsx)(D.a.Trash,null))),se&&Object(F.jsx)(C.a,{id:"export-action-tooltip",title:Object(d.e)("Export"),placement:"bottom"},Object(F.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>de([e])},Object(F.jsx)(D.a.Share,null))),ee&&Object(F.jsx)(C.a,{id:"edit-action-tooltip",title:Object(d.e)("Edit"),placement:"bottom"},Object(F.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>ce(e)},Object(F.jsx)(D.a.EditAlt,null)))):null,Header:Object(d.e)("Actions"),id:"actions",hidden:!ee&&!te,disableSortBy:!0}],[ee,te,se,ce]),re=Object(u.useMemo)(()=>[{Header:Object(d.e)("Owner"),id:"owners",input:"select",operator:f.a.relationManyMany,unfilteredLabel:"All",fetchSelects:Object(m.g)("dataset","owners",Object(m.e)(e=>Object(d.e)("An error occurred while fetching dataset owner values: %s",e)),a.userId),paginate:!0},{Header:Object(d.e)("Database"),id:"database",input:"select",operator:f.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(m.g)("dataset","database",Object(m.e)(e=>Object(d.e)("An error occurred while fetching datasets: %s",e))),paginate:!0},{Header:Object(d.e)("Schema"),id:"schema",input:"select",operator:f.a.equals,unfilteredLabel:"All",fetchSelects:Object(m.f)("dataset","schema",Object(m.e)(e=>Object(d.e)("An error occurred while fetching schema values: %s",e))),paginate:!0},{Header:Object(d.e)("Type"),id:"sql",input:"select",operator:f.a.datasetIsNullOrEmpty,unfilteredLabel:"All",selects:[{label:"Virtual",value:!1},{label:"Physical",value:!0}]},{Header:Object(d.e)("Search"),id:"table_name",input:"search",operator:f.a.contains}],[]),ie={activeChild:"Datasets",...k.a},oe=[];(te||se)&&oe.push({name:Object(d.e)("Bulk select"),onClick:E,buttonStyle:"secondary"}),ae&&oe.push({name:Object(F.jsx)(j.a.Fragment,null,Object(F.jsx)("i",{className:"fa fa-plus"})," ",Object(d.e)("Dataset")," "),onClick:()=>M(!0),buttonStyle:"primary"}),Object(T.c)(T.a.VERSIONED_EXPORT)&&oe.push({name:Object(F.jsx)(C.a,{id:"import-tooltip",title:Object(d.e)("Import datasets"),placement:"bottomRight"},Object(F.jsx)(D.a.Import,null)),buttonStyle:"link",onClick:Z}),ie.buttons=oe;const de=e=>{const t=i()(e).call(e,({id:e})=>e);Object(w.a)("dataset",t,()=>{Y(!1)}),Y(!0)};return Object(F.jsx)(j.a.Fragment,null,Object(F.jsx)(S.a,ie),Object(F.jsx)(U,{show:I,onHide:()=>M(!1),onDatasetAdd:B}),R&&Object(F.jsx)(y.a,{description:Object(d.e)("The dataset %s is linked to %s charts that appear on %s dashboards. Are you sure you want to continue? Deleting the dataset will break those objects.",R.table_name,R.chart_count,R.dashboard_count),onConfirm:()=>{R&&(({id:a,table_name:s})=>{b.a.delete({endpoint:`/api/v1/dataset/${a}`}).then(()=>{B(),z(null),t(Object(d.e)("Deleted: %s",s))},Object(m.e)(t=>e(Object(d.e)("There was an issue deleting %s: %s",s,t))))})(R)},onHide:()=>{z(null)},open:!0,title:Object(d.e)("Delete Dataset?")}),P&&Object(F.jsx)(x.a,{datasource:P,onDatasourceSave:B,onHide:()=>{J(null)},show:!0}),Object(F.jsx)(g.a,{title:Object(d.e)("Please confirm"),description:Object(d.e)("Are you sure you want to delete the selected datasets?"),onConfirm:a=>{b.a.delete({endpoint:`/api/v1/dataset/?q=${p.a.encode(i()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{B(),t(e.message)},Object(m.e)(t=>e(Object(d.e)("There was an issue deleting the selected datasets: %s",t))))}},e=>{const t=[];return te&&t.push({key:"delete",name:Object(d.e)("Delete"),onSelect:e,type:"danger"}),se&&t.push({key:"export",name:Object(d.e)("Export"),type:"primary",onSelect:de}),Object(F.jsx)(f.b,{className:"dataset-list-view",columns:ne,data:r,count:c,pageSize:q.b,fetchData:_,filters:re,loading:s,initialSort:le,bulkActions:t,bulkSelectEnabled:o,disableBulkSelect:E,renderBulkSelectCopy:e=>{const{virtualCount:t,physicalCount:a}=l()(e).call(e,(e,t)=>("physical"===t.original.kind?e.physicalCount+=1:"virtual"===t.original.kind&&(e.virtualCount+=1),e),{virtualCount:0,physicalCount:0});return e.length?t&&!a?Object(d.e)("%s Selected (Virtual)",e.length,t):a&&!t?Object(d.e)("%s Selected (Physical)",e.length,a):Object(d.e)("%s Selected (%s Physical, %s Virtual)",e.length,a,t):Object(d.e)("0 Selected")}})}),Object(F.jsx)($.a,{resourceName:"dataset",resourceLabel:Object(d.e)("dataset"),passwordsNeededMessage:q.c,confirmOverwriteMessage:q.a,addDangerToast:e,addSuccessToast:t,onModelImport:()=>{W(!1),B()},show:Q,onHide:()=>{W(!1)},passwordFields:X,setPasswordFields:G}),K&&Object(F.jsx)(v.a,null))})}}]);