(window.webpackJsonp=window.webpackJsonp||[]).push([[23],{4681:function(e,t,a){"use strict";a.d(t,"a",(function(){return b}));var n=a(11),o=a.n(n),c=(a(0),a(40)),l=a(51),i=a(31),s=a(1);const r=c.g.span`
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
`,d=c.g.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function b({actions:e}){return Object(s.jsx)(r,{className:"actions"},o()(e).call(e,(e,t)=>{const a=i.a[e.icon];return e.tooltip?Object(s.jsx)(l.a,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},Object(s.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},Object(s.jsx)(a,null))):Object(s.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},Object(s.jsx)(a,null))}))}},5071:function(e,t,a){"use strict";a.r(t);a(41);var n=a(35),o=a.n(n),c=a(11),l=a.n(c),i=a(0),s=a.n(i),r=a(111),d=a.n(r),b=a(13),j=a(66),u=a(365),m=a(349),O=a(37),p=a.n(O),g=a(418),h=a(117),x=a(142),y=a(720),f=a(4681),w=a(4669),C=a(45),S=a(961),D=a(1584),v=a(40),k=a(31),$=a(114),_=a(1);const A=v.g.div`
  margin: ${({theme:e})=>2*e.gridUnit}px auto
    ${({theme:e})=>4*e.gridUnit}px auto;
`,H=v.g.div`
  margin-bottom: ${({theme:e})=>10*e.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  textarea,
  input[type='text'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    width: 50%;
  }

  input,
  textarea {
    flex: 1 1 auto;
  }

  textarea {
    width: 100%;
    height: 160px;
    resize: none;
  }

  input::placeholder,
  textarea::placeholder {
    color: ${({theme:e})=>e.colors.grayscale.light1};
  }
`;var M=Object(x.a)(({addDangerToast:e,onLayerAdd:t,onHide:a,show:n,layer:o=null})=>{const[c,l]=Object(i.useState)(!0),[s,r]=Object(i.useState)(),[d,j]=Object(i.useState)(!0),u=null!==o,{state:{loading:m,resource:O},fetchResource:p,createResource:x,updateResource:y}=Object(g.l)("annotation_layer",Object(b.e)("annotation_layer"),e),f=()=>{r({name:"",descr:""})},w=()=>{j(!0),f(),a()},C=e=>{const{target:t}=e,a={...s,name:s?s.name:"",descr:s?s.descr:""};a[t.name]=t.value,r(a)};return Object(i.useEffect)(()=>{if(u&&(!s||!s.id||o&&o.id!==s.id||d&&n)){if(n&&o&&null!==o.id&&!m){const e=o.id||0;p(e)}}else!u&&(!s||s.id||d&&n)&&f()},[o,n]),Object(i.useEffect)(()=>{O&&r(O)},[O]),Object(i.useEffect)(()=>{s&&s.name.length?l(!1):l(!0)},[s?s.name:"",s?s.descr:""]),d&&n&&j(!1),Object(_.jsx)($.b,{disablePrimaryButton:c,onHandledPrimaryAction:()=>{if(u){if(s&&s.id){const e=s.id;delete s.id,delete s.created_by,y(e,s).then(e=>{e&&w()})}}else s&&x(s).then(e=>{e&&(t&&t(e),w())})},onHide:w,primaryButtonName:u?Object(b.e)("Save"):Object(b.e)("Add"),show:n,width:"55%",title:Object(_.jsx)("h4",null,u?Object(_.jsx)(k.a.EditAlt,{css:h.d}):Object(_.jsx)(k.a.PlusLarge,{css:h.d}),u?Object(b.e)("Edit annotation layer properties"):Object(b.e)("Add annotation layer"))},Object(_.jsx)(A,null,Object(_.jsx)("h4",null,Object(b.e)("Basic information"))),Object(_.jsx)(H,null,Object(_.jsx)("div",{className:"control-label"},Object(b.e)("Annotation layer name"),Object(_.jsx)("span",{className:"required"},"*")),Object(_.jsx)("input",{name:"name",onChange:C,type:"text",value:null==s?void 0:s.name})),Object(_.jsx)(H,null,Object(_.jsx)("div",{className:"control-label"},Object(b.e)("description")),Object(_.jsx)("textarea",{name:"descr",value:null==s?void 0:s.descr,placeholder:Object(b.e)("Description (this can be seen in the list)"),onChange:C})))});t.default=Object(x.a)((function({addDangerToast:e,addSuccessToast:t,user:a}){const{state:{loading:n,resourceCount:c,resourceCollection:r,bulkSelectEnabled:O},hasPerm:x,fetchData:v,refreshData:k,toggleBulkSelect:$}=Object(g.k)("annotation_layer",Object(b.e)("Annotation layers"),e),[A,H]=Object(i.useState)(!1),[N,T]=Object(i.useState)(null),[U,Y]=Object(i.useState)(null),E=x("can_write"),B=x("can_write"),z=x("can_write");function L(e){T(e),H(!0)}const F=[{id:"name",desc:!0}],P=Object(i.useMemo)(()=>[{accessor:"name",Header:Object(b.e)("Name"),Cell:({row:{original:{id:e,name:t}}})=>{let a=!0;try{Object(u.f)()}catch(e){a=!1}return a?Object(_.jsx)(m.b,{to:`/annotationmodelview/${e}/annotation`},t):Object(_.jsx)("a",{href:`/annotationmodelview/${e}/annotation`},t)}},{accessor:"descr",Header:Object(b.e)("Description")},{Cell:({row:{original:{changed_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return p()(a).format("MMM DD, YYYY")},Header:Object(b.e)("Last modified"),accessor:"changed_on",size:"xl"},{Cell:({row:{original:{created_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return p()(a).format("MMM DD, YYYY")},Header:Object(b.e)("Created on"),accessor:"created_on",size:"xl"},{accessor:"created_by",disableSortBy:!0,Header:Object(b.e)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:e}})=>{var t;const a=o()(t=[B?{label:"edit-action",tooltip:Object(b.e)("Edit template"),placement:"bottom",icon:"Edit",onClick:()=>L(e)}:null,z?{label:"delete-action",tooltip:Object(b.e)("Delete template"),placement:"bottom",icon:"Trash",onClick:()=>Y(e)}:null]).call(t,e=>!!e);return Object(_.jsx)(f.a,{actions:a})},Header:Object(b.e)("Actions"),id:"actions",disableSortBy:!0,hidden:!B&&!z,size:"xl"}],[z,E]),q=[];E&&q.push({name:Object(_.jsx)(s.a.Fragment,null,Object(_.jsx)("i",{className:"fa fa-plus"})," ",Object(b.e)("Annotation layer")),buttonStyle:"primary",onClick:()=>{L(null)}}),z&&q.push({name:Object(b.e)("Bulk select"),onClick:$,buttonStyle:"secondary"});const I=Object(i.useMemo)(()=>[{Header:Object(b.e)("Created by"),id:"created_by",input:"select",operator:w.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(h.g)("annotation_layer","created_by",Object(h.e)(e=>Object(b.e)("An error occurred while fetching dataset datasource values: %s",e)),a.userId),paginate:!0},{Header:Object(b.e)("Search"),id:"name",input:"search",operator:w.a.contains}],[]),R=Object(_.jsx)(C.a,{buttonStyle:"primary",onClick:()=>{L(null)}},Object(_.jsx)(s.a.Fragment,null,Object(_.jsx)("i",{className:"fa fa-plus"})," ",Object(b.e)("Annotation layer"))),J={message:Object(b.e)("No annotation layers yet"),slot:R};return Object(_.jsx)(s.a.Fragment,null,Object(_.jsx)(y.a,{name:Object(b.e)("Annotation layers"),buttons:q}),Object(_.jsx)(M,{addDangerToast:e,layer:N,onLayerAdd:e=>{window.location.href=`/annotationmodelview/${e}/annotation`},onHide:()=>{k(),H(!1)},show:A}),U&&Object(_.jsx)(S.a,{description:Object(b.e)("This action will permanently delete the layer."),onConfirm:()=>{U&&(({id:a,name:n})=>{j.a.delete({endpoint:`/api/v1/annotation_layer/${a}`}).then(()=>{k(),Y(null),t(Object(b.e)("Deleted: %s",n))},Object(h.e)(t=>e(Object(b.e)("There was an issue deleting %s: %s",n,t))))})(U)},onHide:()=>Y(null),open:!0,title:Object(b.e)("Delete Layer?")}),Object(_.jsx)(D.a,{title:Object(b.e)("Please confirm"),description:Object(b.e)("Are you sure you want to delete the selected layers?"),onConfirm:a=>{j.a.delete({endpoint:`/api/v1/annotation_layer/?q=${d.a.encode(l()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{k(),t(e.message)},Object(h.e)(t=>e(Object(b.e)("There was an issue deleting the selected layers: %s",t))))}},e=>{const t=z?[{key:"delete",name:Object(b.e)("Delete"),onSelect:e,type:"danger"}]:[];return Object(_.jsx)(w.b,{className:"annotation-layers-list-view",columns:P,count:c,data:r,fetchData:v,filters:I,initialSort:F,loading:n,pageSize:25,bulkActions:t,bulkSelectEnabled:O,disableBulkSelect:$,emptyState:J})}))}))}}]);