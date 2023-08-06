(window.webpackJsonp=window.webpackJsonp||[]).push([[25],{4682:function(e,t,a){"use strict";a(41);var l=a(11),r=a.n(l),s=a(35),c=a.n(s),n=a(0),o=a.n(n),i=a(40),d=a(13),b=a(45),u=a(114),j=a(19),m=a(418),p=a(1);const O=i.g.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,h=i.g.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:l,addDangerToast:s,addSuccessToast:i,onModelImport:g,show:x,onHide:y,passwordFields:f=[],setPasswordFields:v=(()=>{})})=>{const[w,_]=Object(n.useState)(!0),[S,C]=Object(n.useState)({}),[E,I]=Object(n.useState)(!1),[T,k]=Object(n.useState)(!1),[N,$]=Object(n.useState)([]),[A,H]=Object(n.useState)(!1),z=()=>{$([]),v([]),C({}),I(!1),k(!1),H(!1)},{state:{alreadyExists:F,passwordsNeeded:D},importResource:M}=Object(m.j)(e,t,e=>{z(),s(e)});Object(n.useEffect)(()=>{v(D),D.length>0&&H(!1)},[D,v]),Object(n.useEffect)(()=>{I(F.length>0),F.length>0&&H(!1)},[F,I]);const R=e=>{var t,a;const l=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";k(l.toUpperCase()===Object(d.e)("OVERWRITE"))};return w&&x&&_(!1),Object(p.jsx)(u.b,{name:"model",className:"import-model-modal",disablePrimaryButton:0===N.length||E&&!T||A,onHandledPrimaryAction:()=>{var e;(null==(e=N[0])?void 0:e.originFileObj)instanceof File&&(H(!0),M(N[0].originFileObj,S,T).then(e=>{e&&(i(Object(d.e)("The import was successful")),z(),g())}))},onHide:()=>{_(!0),y(),z()},primaryButtonName:E?Object(d.e)("Overwrite"):Object(d.e)("Import"),primaryButtonType:E?"danger":"primary",width:"750px",show:x,title:Object(p.jsx)("h4",null,Object(d.e)("Import %s",t))},Object(p.jsx)(h,null,Object(p.jsx)(j.F,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:N,onChange:e=>{$([{...e.file,status:"done"}])},onRemove:e=>($(c()(N).call(N,t=>t.uid!==e.uid)),!1),customRequest:()=>{}},Object(p.jsx)(b.a,{loading:A},"Select file"))),0===f.length?null:Object(p.jsx)(o.a.Fragment,null,Object(p.jsx)("h5",null,"Database passwords"),Object(p.jsx)(O,null,a),r()(f).call(f,e=>Object(p.jsx)(h,{key:`password-for-${e}`},Object(p.jsx)("div",{className:"control-label"},e,Object(p.jsx)("span",{className:"required"},"*")),Object(p.jsx)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:S[e],onChange:t=>C({...S,[e]:t.target.value})})))),E?Object(p.jsx)(o.a.Fragment,null,Object(p.jsx)(h,null,Object(p.jsx)("div",{className:"confirm-overwrite"},l),Object(p.jsx)("div",{className:"control-label"},Object(d.e)('Type "%s" to confirm',Object(d.e)("OVERWRITE"))),Object(p.jsx)("input",{id:"overwrite",type:"text",onChange:R}))):null)}},4959:function(e,t,a){var l=a(669),r=a(4613);e.exports=function(e,t){return e&&e.length?r(e,l(t,2)):[]}},5041:function(e,t,a){"use strict";a.r(t);a(41);var l=a(110),r=a.n(l),s=a(35),c=a.n(s),n=a(161),o=a.n(n),i=a(11),d=a.n(i),b=a(4959),u=a.n(b),j=a(13),m=a(194),p=a(66),O=a(40),h=a(0),g=a.n(h),x=a(111),y=a.n(x),f=a(37),v=a.n(f),w=a(42),_=a(117),S=a(418),C=a(1585),E=a(1584),I=a(720),T=a(1110),k=a(4669),N=a(171),$=a(216),A=a(142),H=a(1561),z=a(4682),F=a(51),D=a(31),M=a(636),R=a(2168),U=a(1);const B=Object(j.e)('The passwords for the databases below are needed in order to import them together with the charts. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),L=Object(j.e)("You are importing one or more charts that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),P=Object(m.a)(),V=O.g.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(A.a)((function(e){var t,a,l;const{addDangerToast:s,addSuccessToast:n}=e,{state:{loading:i,resourceCount:b,resourceCollection:m,bulkSelectEnabled:O},setResourceCollection:x,hasPerm:f,fetchData:A,toggleBulkSelect:q,refreshData:W}=Object(S.k)("chart",Object(j.e)("chart"),s),J=Object(h.useMemo)(()=>d()(m).call(m,e=>e.id),[m]),[X,Y]=Object(S.i)("chart",J,s),{sliceCurrentlyEditing:G,handleChartUpdated:K,openChartEditModal:Q,closeChartEditModal:Z}=Object(S.g)(x,m),[ee,te]=Object(h.useState)(!1),[ae,le]=Object(h.useState)([]),[re,se]=Object(h.useState)(!1),{userId:ce}=e.user,ne=Object($.a)(ce.toString(),null),oe=()=>{te(!0)},ie=f("can_write"),de=f("can_write"),be=f("can_write"),ue=f("can_read")&&Object(w.c)(w.a.VERSIONED_EXPORT),je=[{id:"changed_on_delta_humanized",desc:!0}],me=e=>{const t=d()(e).call(e,({id:e})=>e);Object(C.a)("chart",t,()=>{se(!1)}),se(!0)},pe=Object(h.useMemo)(()=>[...e.user.userId?[{Cell:({row:{original:{id:e}}})=>Object(U.jsx)(T.a,{itemId:e,saveFaveStar:X,isStarred:Y[e]}),Header:"",id:"id",disableSortBy:!0,size:"xs"}]:[],{Cell:({row:{original:{url:e,slice_name:t}}})=>Object(U.jsx)("a",{href:e},t),Header:Object(j.e)("Chart"),accessor:"slice_name"},{Cell:({row:{original:{viz_type:e}}})=>{var t;return(null==(t=P.get(e))?void 0:t.name)||e},Header:Object(j.e)("Visualization type"),accessor:"viz_type",size:"xxl"},{Cell:({row:{original:{datasource_name_text:e,datasource_url:t}}})=>Object(U.jsx)("a",{href:t},e),Header:Object(j.e)("Dataset"),accessor:"datasource_id",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{last_saved_by:e,changed_by_url:t}}})=>Object(U.jsx)("a",{href:t},null!=e&&e.first_name?`${null==e?void 0:e.first_name} ${null==e?void 0:e.last_name}`:null),Header:Object(j.e)("Modified by"),accessor:"last_saved_by.first_name",size:"xl"},{Cell:({row:{original:{last_saved_at:e}}})=>Object(U.jsx)("span",{className:"no-wrap"},e?v.a.utc(e).fromNow():null),Header:Object(j.e)("Last modified"),accessor:"last_saved_at",size:"xl"},{accessor:"owners",hidden:!0,disableSortBy:!0},{Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",Header:Object(j.e)("Created by"),accessor:"created_by",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>de||be||ue?Object(U.jsx)(V,{className:"actions"},be&&Object(U.jsx)(E.a,{title:Object(j.e)("Please confirm"),description:Object(U.jsx)(g.a.Fragment,null,Object(j.e)("Are you sure you want to delete")," ",Object(U.jsx)("b",null,e.slice_name),"?"),onConfirm:()=>Object(_.m)(e,n,s,W)},e=>Object(U.jsx)(F.a,{id:"delete-action-tooltip",title:Object(j.e)("Delete"),placement:"bottom"},Object(U.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},Object(U.jsx)(D.a.Trash,null)))),ue&&Object(U.jsx)(F.a,{id:"export-action-tooltip",title:Object(j.e)("Export"),placement:"bottom"},Object(U.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>me([e])},Object(U.jsx)(D.a.Share,null))),de&&Object(U.jsx)(F.a,{id:"edit-action-tooltip",title:Object(j.e)("Edit"),placement:"bottom"},Object(U.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>Q(e)},Object(U.jsx)(D.a.EditAlt,null)))):null,Header:Object(j.e)("Actions"),id:"actions",disableSortBy:!0,hidden:!de&&!be}],[de,be,ue,...e.user.userId?[Y]:[]]),Oe={Header:Object(j.e)("Favorite"),id:"id",urlDisplay:"favorite",input:"select",operator:k.a.chartIsFav,unfilteredLabel:Object(j.e)("Any"),selects:[{label:Object(j.e)("Yes"),value:!0},{label:Object(j.e)("No"),value:!1}]},he=[{Header:Object(j.e)("Owner"),id:"owners",input:"select",operator:k.a.relationManyMany,unfilteredLabel:Object(j.e)("All"),fetchSelects:Object(_.g)("chart","owners",Object(_.e)(e=>s(Object(j.e)("An error occurred while fetching chart owners values: %s",e))),e.user.userId),paginate:!0},{Header:Object(j.e)("Created by"),id:"created_by",input:"select",operator:k.a.relationOneMany,unfilteredLabel:Object(j.e)("All"),fetchSelects:Object(_.g)("chart","created_by",Object(_.e)(e=>s(Object(j.e)("An error occurred while fetching chart created by values: %s",e))),e.user.userId),paginate:!0},{Header:Object(j.e)("Viz type"),id:"viz_type",input:"select",operator:k.a.equals,unfilteredLabel:Object(j.e)("All"),selects:o()(t=d()(a=c()(l=r()(P).call(P)).call(l,e=>{var t;return Object(M.e)((null==(t=P.get(e))?void 0:t.behaviors)||[])})).call(a,e=>{var t;return{label:(null==(t=P.get(e))?void 0:t.name)||e,value:e}})).call(t,(e,t)=>e.label&&t.label?e.label>t.label?1:e.label<t.label?-1:0:0)},{Header:Object(j.e)("Dataset"),id:"datasource_id",input:"select",operator:k.a.equals,unfilteredLabel:Object(j.e)("All"),fetchSelects:(ge=Object(_.e)(e=>s(Object(j.e)("An error occurred while fetching chart dataset values: %s",e))),async(e="",t,a)=>{const l=e?{filters:[{col:"table_name",opr:"sw",value:e}]}:{};try{var r;const e=y.a.encode({columns:["datasource_name","datasource_id"],keys:["none"],order_column:"table_name",order_direction:"asc",...t?{page:t}:{},...a?{page_size:a}:{},...l}),{json:s={}}=await p.a.get({endpoint:`/api/v1/dataset/?q=${e}`}),c=null==s?void 0:null==(r=s.result)?void 0:d()(r).call(r,({table_name:e,id:t})=>({label:e,value:t}));return u()(c,"value")}catch(e){ge(e)}return[]}),paginate:!0},...e.user.userId?[Oe]:[],{Header:Object(j.e)("Search"),id:"slice_name",input:"search",operator:k.a.chartAllText}];var ge;const xe=[{desc:!1,id:"slice_name",label:Object(j.e)("Alphabetical"),value:"alphabetical"},{desc:!0,id:"changed_on_delta_humanized",label:Object(j.e)("Recently modified"),value:"recently_modified"},{desc:!1,id:"changed_on_delta_humanized",label:Object(j.e)("Least recently modified"),value:"least_recently_modified"}];function ye(e){return Object(U.jsx)(R.a,{chart:e,showThumbnails:ne?ne.thumbnails:Object(w.c)(w.a.THUMBNAILS),hasPerm:f,openChartEditModal:Q,bulkSelectEnabled:O,addDangerToast:s,addSuccessToast:n,refreshData:W,loading:i,favoriteStatus:Y[e.id],saveFavoriteStatus:X,handleBulkChartExport:me})}const fe=[];return(be||ue)&&fe.push({name:Object(j.e)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:q}),ie&&fe.push({name:Object(U.jsx)(g.a.Fragment,null,Object(U.jsx)("i",{className:"fa fa-plus"})," ",Object(j.e)("Chart")),buttonStyle:"primary",onClick:()=>{window.location.assign("/chart/add")}}),Object(w.c)(w.a.VERSIONED_EXPORT)&&fe.push({name:Object(U.jsx)(F.a,{id:"import-tooltip",title:Object(j.e)("Import charts"),placement:"bottomRight"},Object(U.jsx)(D.a.Import,null)),buttonStyle:"link",onClick:oe}),Object(U.jsx)(g.a.Fragment,null,Object(U.jsx)(I.a,{name:Object(j.e)("Charts"),buttons:fe}),G&&Object(U.jsx)(H.a,{onHide:Z,onSave:K,show:!0,slice:G}),Object(U.jsx)(E.a,{title:Object(j.e)("Please confirm"),description:Object(j.e)("Are you sure you want to delete the selected charts?"),onConfirm:function(e){p.a.delete({endpoint:`/api/v1/chart/?q=${y.a.encode(d()(e).call(e,({id:e})=>e))}`}).then(({json:e={}})=>{W(),n(e.message)},Object(_.e)(e=>s(Object(j.e)("There was an issue deleting the selected charts: %s",e))))}},e=>{const t=[];return be&&t.push({key:"delete",name:Object(j.e)("Delete"),type:"danger",onSelect:e}),ue&&t.push({key:"export",name:Object(j.e)("Export"),type:"primary",onSelect:me}),Object(U.jsx)(k.b,{bulkActions:t,bulkSelectEnabled:O,cardSortSelectOptions:xe,className:"chart-list-view",columns:pe,count:b,data:m,disableBulkSelect:q,fetchData:A,filters:he,initialSort:je,loading:i,pageSize:25,renderCard:ye,showThumbnails:ne?ne.thumbnails:Object(w.c)(w.a.THUMBNAILS),defaultViewMode:Object(w.c)(w.a.LISTVIEWS_DEFAULT_CARD_VIEW)?"card":"table"})}),Object(U.jsx)(z.a,{resourceName:"chart",resourceLabel:Object(j.e)("chart"),passwordsNeededMessage:B,confirmOverwriteMessage:L,addDangerToast:s,addSuccessToast:n,onModelImport:()=>{te(!1),W()},show:ee,onHide:()=>{te(!1)},passwordFields:ae,setPasswordFields:le}),re&&Object(U.jsx)(N.a,null))}))}}]);