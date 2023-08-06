(window.webpackJsonp=window.webpackJsonp||[]).push([[28],{4682:function(e,t,a){"use strict";a(41);var s=a(11),r=a.n(s),o=a(35),l=a.n(o),n=a(0),c=a.n(n),d=a(40),i=a(13),b=a(45),u=a(114),j=a(19),h=a(418),O=a(1);const m=d.g.div`
  display: block;
  color: ${({theme:e})=>e.colors.grayscale.base};
  font-size: ${({theme:e})=>e.typography.sizes.s-1}px;
`,p=d.g.div`
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
`;t.a=({resourceName:e,resourceLabel:t,passwordsNeededMessage:a,confirmOverwriteMessage:s,addDangerToast:o,addSuccessToast:d,onModelImport:g,show:x,onHide:y,passwordFields:f=[],setPasswordFields:w=(()=>{})})=>{const[_,S]=Object(n.useState)(!0),[v,C]=Object(n.useState)({}),[I,T]=Object(n.useState)(!1),[E,k]=Object(n.useState)(!1),[D,F]=Object(n.useState)([]),[H,N]=Object(n.useState)(!1),$=()=>{F([]),w([]),C({}),T(!1),k(!1),N(!1)},{state:{alreadyExists:A,passwordsNeeded:z},importResource:M}=Object(h.j)(e,t,e=>{$(),o(e)});Object(n.useEffect)(()=>{w(z),z.length>0&&N(!1)},[z,w]),Object(n.useEffect)(()=>{T(A.length>0),A.length>0&&N(!1)},[A,T]);const U=e=>{var t,a;const s=null!=(t=null==(a=e.currentTarget)?void 0:a.value)?t:"";k(s.toUpperCase()===Object(i.e)("OVERWRITE"))};return _&&x&&S(!1),Object(O.jsx)(u.b,{name:"model",className:"import-model-modal",disablePrimaryButton:0===D.length||I&&!E||H,onHandledPrimaryAction:()=>{var e;(null==(e=D[0])?void 0:e.originFileObj)instanceof File&&(N(!0),M(D[0].originFileObj,v,E).then(e=>{e&&(d(Object(i.e)("The import was successful")),$(),g())}))},onHide:()=>{S(!0),y(),$()},primaryButtonName:I?Object(i.e)("Overwrite"):Object(i.e)("Import"),primaryButtonType:I?"danger":"primary",width:"750px",show:x,title:Object(O.jsx)("h4",null,Object(i.e)("Import %s",t))},Object(O.jsx)(p,null,Object(O.jsx)(j.F,{name:"modelFile",id:"modelFile",accept:".yaml,.json,.yml,.zip",fileList:D,onChange:e=>{F([{...e.file,status:"done"}])},onRemove:e=>(F(l()(D).call(D,t=>t.uid!==e.uid)),!1),customRequest:()=>{}},Object(O.jsx)(b.a,{loading:H},"Select file"))),0===f.length?null:Object(O.jsx)(c.a.Fragment,null,Object(O.jsx)("h5",null,"Database passwords"),Object(O.jsx)(m,null,a),r()(f).call(f,e=>Object(O.jsx)(p,{key:`password-for-${e}`},Object(O.jsx)("div",{className:"control-label"},e,Object(O.jsx)("span",{className:"required"},"*")),Object(O.jsx)("input",{name:`password-${e}`,autoComplete:`password-${e}`,type:"password",value:v[e],onChange:t=>C({...v,[e]:t.target.value})})))),I?Object(O.jsx)(c.a.Fragment,null,Object(O.jsx)(p,null,Object(O.jsx)("div",{className:"confirm-overwrite"},s),Object(O.jsx)("div",{className:"control-label"},Object(i.e)('Type "%s" to confirm',Object(i.e)("OVERWRITE"))),Object(O.jsx)("input",{id:"overwrite",type:"text",onChange:U}))):null)}},5074:function(e,t,a){"use strict";a.r(t);a(41);var s,r=a(11),o=a.n(r),l=a(13),n=a(40),c=a(66),d=a(0),i=a.n(d),b=a(349),u=a(111),j=a.n(u),h=a(42),O=a(117),m=a(418),p=a(1584),g=a(1585),x=a(171),y=a(720),f=a(4669),w=a(216),_=a(142),S=a(672),v=a(31),C=a(1110),I=a(1970),T=a(51),E=a(4682),k=a(2169);!function(e){e.PUBLISHED="published",e.DRAFT="draft"}(s||(s={}));var D=a(1);const F=Object(l.e)('The passwords for the databases below are needed in order to import them together with the dashboards. Please note that the "Secure Extra" and "Certificate" sections of the database configuration are not present in export files, and should be added manually after the import if they are needed.'),H=Object(l.e)("You are importing one or more dashboards that already exist. Overwriting might cause you to lose some of your work. Are you sure you want to overwrite?"),N=n.g.div`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;t.default=Object(_.a)((function(e){const{addDangerToast:t,addSuccessToast:a}=e,{state:{loading:r,resourceCount:n,resourceCollection:u,bulkSelectEnabled:_},setResourceCollection:$,hasPerm:A,fetchData:z,toggleBulkSelect:M,refreshData:U}=Object(m.k)("dashboard",Object(l.e)("dashboard"),t),B=Object(d.useMemo)(()=>o()(u).call(u,e=>e.id),[u]),[L,P]=Object(m.i)("dashboard",B,t),[R,V]=Object(d.useState)(null),[q,W]=Object(d.useState)(!1),[J,Y]=Object(d.useState)([]),[X,G]=Object(d.useState)(!1),K=()=>{W(!0)},{userId:Q}=e.user,Z=Object(w.a)(Q.toString(),null),ee=A("can_write"),te=A("can_write"),ae=A("can_write"),se=A("can_read"),re=[{id:"changed_on_delta_humanized",desc:!0}];function oe(e){V(e)}function le(e){return c.a.get({endpoint:`/api/v1/dashboard/${e.id}`}).then(({json:e={}})=>{$(o()(u).call(u,t=>{var a;if(t.id===(null==e?void 0:null==(a=e.result)?void 0:a.id)){const{changed_by_name:a,changed_by_url:s,changed_by:r,dashboard_title:o="",slug:l="",json_metadata:n="",changed_on_delta_humanized:c,url:d=""}=e.result;return{...t,changed_by_name:a,changed_by_url:s,changed_by:r,dashboard_title:o,slug:l,json_metadata:n,changed_on_delta_humanized:c,url:d}}return t}))},Object(O.e)(e=>t(Object(l.e)("An error occurred while fetching dashboards: %s",e))))}const ne=e=>{const t=o()(e).call(e,({id:e})=>e);Object(g.a)("dashboard",t,()=>{G(!1)}),G(!0)},ce=Object(d.useMemo)(()=>[...e.user.userId?[{Cell:({row:{original:{id:e}}})=>Object(D.jsx)(C.a,{itemId:e,saveFaveStar:L,isStarred:P[e]}),Header:"",id:"id",disableSortBy:!0,size:"xs"}]:[],{Cell:({row:{original:{url:e,dashboard_title:t}}})=>Object(D.jsx)(b.b,{to:e},t),Header:Object(l.e)("Title"),accessor:"dashboard_title"},{Cell:({row:{original:{changed_by_name:e,changed_by_url:t}}})=>Object(D.jsx)("a",{href:t},e),Header:Object(l.e)("Modified by"),accessor:"changed_by.first_name",size:"xl"},{Cell:({row:{original:{status:e}}})=>e===s.PUBLISHED?Object(l.e)("Published"):Object(l.e)("Draft"),Header:Object(l.e)("Status"),accessor:"published",size:"xl"},{Cell:({row:{original:{changed_on_delta_humanized:e}}})=>Object(D.jsx)("span",{className:"no-wrap"},e),Header:Object(l.e)("Modified"),accessor:"changed_on_delta_humanized",size:"xl"},{Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",Header:Object(l.e)("Created by"),accessor:"created_by",disableSortBy:!0,size:"xl"},{Cell:({row:{original:{owners:e=[]}}})=>Object(D.jsx)(S.a,{users:e}),Header:Object(l.e)("Owners"),accessor:"owners",disableSortBy:!0,size:"xl"},{Cell:({row:{original:e}})=>Object(D.jsx)(N,{className:"actions"},ae&&Object(D.jsx)(p.a,{title:Object(l.e)("Please confirm"),description:Object(D.jsx)(i.a.Fragment,null,Object(l.e)("Are you sure you want to delete")," ",Object(D.jsx)("b",null,e.dashboard_title),"?"),onConfirm:()=>Object(O.n)(e,U,a,t)},e=>Object(D.jsx)(T.a,{id:"delete-action-tooltip",title:Object(l.e)("Delete"),placement:"bottom"},Object(D.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:e},Object(D.jsx)(v.a.Trash,null)))),se&&Object(D.jsx)(T.a,{id:"export-action-tooltip",title:Object(l.e)("Export"),placement:"bottom"},Object(D.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>ne([e])},Object(D.jsx)(v.a.Share,null))),te&&Object(D.jsx)(T.a,{id:"edit-action-tooltip",title:Object(l.e)("Edit"),placement:"bottom"},Object(D.jsx)("span",{role:"button",tabIndex:0,className:"action-button",onClick:()=>oe(e)},Object(D.jsx)(v.a.EditAlt,null)))),Header:Object(l.e)("Actions"),id:"actions",hidden:!te&&!ae&&!se,disableSortBy:!0}],[te,ae,se,...e.user.userId?[P]:[]]),de={Header:Object(l.e)("Favorite"),id:"id",urlDisplay:"favorite",input:"select",operator:f.a.dashboardIsFav,unfilteredLabel:Object(l.e)("Any"),selects:[{label:Object(l.e)("Yes"),value:!0},{label:Object(l.e)("No"),value:!1}]},ie=[{Header:Object(l.e)("Owner"),id:"owners",input:"select",operator:f.a.relationManyMany,unfilteredLabel:Object(l.e)("All"),fetchSelects:Object(O.g)("dashboard","owners",Object(O.e)(e=>t(Object(l.e)("An error occurred while fetching dashboard owner values: %s",e))),e.user.userId),paginate:!0},{Header:Object(l.e)("Created by"),id:"created_by",input:"select",operator:f.a.relationOneMany,unfilteredLabel:Object(l.e)("All"),fetchSelects:Object(O.g)("dashboard","created_by",Object(O.e)(e=>t(Object(l.e)("An error occurred while fetching dashboard created by values: %s",e))),e.user.userId),paginate:!0},{Header:Object(l.e)("Status"),id:"published",input:"select",operator:f.a.equals,unfilteredLabel:Object(l.e)("Any"),selects:[{label:Object(l.e)("Published"),value:!0},{label:Object(l.e)("Draft"),value:!1}]},...e.user.userId?[de]:[],{Header:Object(l.e)("Search"),id:"dashboard_title",input:"search",operator:f.a.titleOrSlug}],be=[{desc:!1,id:"dashboard_title",label:Object(l.e)("Alphabetical"),value:"alphabetical"},{desc:!0,id:"changed_on_delta_humanized",label:Object(l.e)("Recently modified"),value:"recently_modified"},{desc:!1,id:"changed_on_delta_humanized",label:Object(l.e)("Least recently modified"),value:"least_recently_modified"}];function ue(e){return Object(D.jsx)(k.a,{dashboard:e,hasPerm:A,bulkSelectEnabled:_,refreshData:U,showThumbnails:Z?Z.thumbnails:Object(h.c)(h.a.THUMBNAILS),loading:r,addDangerToast:t,addSuccessToast:a,openDashboardEditModal:oe,saveFavoriteStatus:L,favoriteStatus:P[e.id],handleBulkDashboardExport:ne})}const je=[];return(ae||se)&&je.push({name:Object(l.e)("Bulk select"),buttonStyle:"secondary","data-test":"bulk-select",onClick:M}),ee&&je.push({name:Object(D.jsx)(i.a.Fragment,null,Object(D.jsx)("i",{className:"fa fa-plus"})," ",Object(l.e)("Dashboard")),buttonStyle:"primary",onClick:()=>{window.location.assign("/dashboard/new")}}),Object(h.c)(h.a.VERSIONED_EXPORT)&&je.push({name:Object(D.jsx)(T.a,{id:"import-tooltip",title:Object(l.e)("Import dashboards"),placement:"bottomRight"},Object(D.jsx)(v.a.Import,null)),buttonStyle:"link",onClick:K}),Object(D.jsx)(i.a.Fragment,null,Object(D.jsx)(y.a,{name:Object(l.e)("Dashboards"),buttons:je}),Object(D.jsx)(p.a,{title:Object(l.e)("Please confirm"),description:Object(l.e)("Are you sure you want to delete the selected dashboards?"),onConfirm:function(e){return c.a.delete({endpoint:`/api/v1/dashboard/?q=${j.a.encode(o()(e).call(e,({id:e})=>e))}`}).then(({json:e={}})=>{U(),a(e.message)},Object(O.e)(e=>t(Object(l.e)("There was an issue deleting the selected dashboards: ",e))))}},e=>{const t=[];return ae&&t.push({key:"delete",name:Object(l.e)("Delete"),type:"danger",onSelect:e}),se&&t.push({key:"export",name:Object(l.e)("Export"),type:"primary",onSelect:ne}),Object(D.jsx)(i.a.Fragment,null,R&&Object(D.jsx)(I.a,{dashboardId:R.id,show:!0,onHide:()=>V(null),onSubmit:le}),Object(D.jsx)(f.b,{bulkActions:t,bulkSelectEnabled:_,cardSortSelectOptions:be,className:"dashboard-list-view",columns:ce,count:n,data:u,disableBulkSelect:M,fetchData:z,filters:ie,initialSort:re,loading:r,pageSize:25,showThumbnails:Z?Z.thumbnails:Object(h.c)(h.a.THUMBNAILS),renderCard:ue,defaultViewMode:Object(h.c)(h.a.LISTVIEWS_DEFAULT_CARD_VIEW)?"card":"table"}))}),Object(D.jsx)(E.a,{resourceName:"dashboard",resourceLabel:Object(l.e)("dashboard"),passwordsNeededMessage:F,confirmOverwriteMessage:H,addDangerToast:t,addSuccessToast:a,onModelImport:()=>{W(!1),U()},show:q,onHide:()=>{W(!1)},passwordFields:J,setPasswordFields:Y}),X&&Object(D.jsx)(x.a,null))}))}}]);