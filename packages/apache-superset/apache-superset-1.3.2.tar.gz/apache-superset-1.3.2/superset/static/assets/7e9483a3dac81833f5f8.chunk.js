(window.webpackJsonp=window.webpackJsonp||[]).push([[26],{4681:function(e,t,a){"use strict";a.d(t,"a",(function(){return b}));var l=a(11),s=a.n(l),n=(a(0),a(40)),c=a(51),o=a(31),i=a(1);const r=n.g.span`
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
`,d=n.g.span`
  color: ${({theme:e})=>e.colors.grayscale.base};
`;function b({actions:e}){return Object(i.jsx)(r,{className:"actions"},s()(e).call(e,(e,t)=>{const a=o.a[e.icon];return e.tooltip?Object(i.jsx)(c.a,{id:`${e.label}-tooltip`,title:e.tooltip,placement:e.placement,key:t},Object(i.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick},Object(i.jsx)(a,null))):Object(i.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:e.onClick,key:t},Object(i.jsx)(a,null))}))}},5073:function(e,t,a){"use strict";a.r(t);a(41);var l=a(35),s=a.n(l),n=a(11),c=a.n(n),o=a(0),i=a.n(o),r=a(13),d=a(66),b=a(111),m=a.n(b),u=a(37),j=a.n(u),p=a(418),O=a(117),h=a(142),g=a(720),x=a(961),_=a(51),f=a(1584),S=a(4681),y=a(4669),w=a(40),C=a(31),v=a(114),$=a(310),k=a(1);const D=w.g.div`
  margin: ${({theme:e})=>2*e.gridUnit}px auto
    ${({theme:e})=>4*e.gridUnit}px auto;
`,T=Object(w.g)($.b)`
  border-radius: ${({theme:e})=>e.borderRadius}px;
  border: 1px solid ${({theme:e})=>e.colors.secondary.light2};
`,H=w.g.div`
  margin-bottom: ${({theme:e})=>10*e.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:e})=>2*e.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:e})=>e.gridUnit/2}px;
    color: ${({theme:e})=>e.colors.error.base};
  }

  input[type='text'] {
    padding: ${({theme:e})=>1.5*e.gridUnit}px
      ${({theme:e})=>2*e.gridUnit}px;
    border: 1px solid ${({theme:e})=>e.colors.grayscale.light2};
    border-radius: ${({theme:e})=>e.gridUnit}px;
    width: 50%;
  }
`;var N=Object(h.a)(({addDangerToast:e,onCssTemplateAdd:t,onHide:a,show:l,cssTemplate:s=null})=>{const[n,c]=Object(o.useState)(!0),[i,d]=Object(o.useState)(null),[b,m]=Object(o.useState)(!0),u=null!==s,{state:{loading:j,resource:h},fetchResource:g,createResource:x,updateResource:_}=Object(p.l)("css_template",Object(r.e)("css_template"),e),f=()=>{m(!0),a()};return Object(o.useEffect)(()=>{if(u&&(!i||!i.id||s&&s.id!==i.id||b&&l)){if(s&&null!==s.id&&!j){const e=s.id||0;g(e)}}else!u&&(!i||i.id||b&&l)&&d({template_name:"",css:""})},[s]),Object(o.useEffect)(()=>{h&&d(h)},[h]),Object(o.useEffect)(()=>{i&&i.template_name.length&&i.css&&i.css.length?c(!1):c(!0)},[i?i.template_name:"",i?i.css:""]),b&&l&&m(!1),Object(k.jsx)(v.b,{disablePrimaryButton:n,onHandledPrimaryAction:()=>{if(u){if(i&&i.id){const e=i.id;delete i.id,delete i.created_by,_(e,i).then(e=>{e&&(t&&t(),f())})}}else i&&x(i).then(e=>{e&&(t&&t(),f())})},onHide:f,primaryButtonName:u?Object(r.e)("Save"):Object(r.e)("Add"),show:l,width:"55%",title:Object(k.jsx)("h4",null,u?Object(k.jsx)(C.a.EditAlt,{css:O.d}):Object(k.jsx)(C.a.PlusLarge,{css:O.d}),u?Object(r.e)("Edit CSS template properties"):Object(r.e)("Add CSS template"))},Object(k.jsx)(D,null,Object(k.jsx)("h4",null,Object(r.e)("Basic information"))),Object(k.jsx)(H,null,Object(k.jsx)("div",{className:"control-label"},Object(r.e)("CSS template name"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)("input",{name:"template_name",onChange:e=>{const{target:t}=e,a={...i,template_name:i?i.template_name:"",css:i?i.css:""};a[t.name]=t.value,d(a)},type:"text",value:null==i?void 0:i.template_name})),Object(k.jsx)(H,null,Object(k.jsx)("div",{className:"control-label"},Object(r.e)("css"),Object(k.jsx)("span",{className:"required"},"*")),Object(k.jsx)(T,{onChange:e=>{const t={...i,template_name:i?i.template_name:"",css:e};d(t)},value:null==i?void 0:i.css,width:"100%"})))});t.default=Object(h.a)((function({addDangerToast:e,addSuccessToast:t,user:a}){const{state:{loading:l,resourceCount:n,resourceCollection:b,bulkSelectEnabled:u},hasPerm:h,fetchData:w,refreshData:C,toggleBulkSelect:v}=Object(p.k)("css_template",Object(r.e)("CSS templates"),e),[$,D]=Object(o.useState)(!1),[T,H]=Object(o.useState)(null),A=h("can_write"),B=h("can_write"),E=h("can_write"),[U,z]=Object(o.useState)(null),M=[{id:"template_name",desc:!0}],P=Object(o.useMemo)(()=>[{accessor:"template_name",Header:Object(r.e)("Name")},{Cell:({row:{original:{changed_on_delta_humanized:e,changed_by:t}}})=>{let a="null";return t&&(a=`${t.first_name} ${t.last_name}`),Object(k.jsx)(_.a,{id:"allow-run-async-header-tooltip",title:Object(r.e)("Last modified by %s",a),placement:"right"},Object(k.jsx)("span",null,e))},Header:Object(r.e)("Last modified"),accessor:"changed_on_delta_humanized",size:"xl",disableSortBy:!0},{Cell:({row:{original:{created_on:e}}})=>{const t=new Date(e),a=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return j()(a).fromNow()},Header:Object(r.e)("Created on"),accessor:"created_on",size:"xl",disableSortBy:!0},{accessor:"created_by",disableSortBy:!0,Header:Object(r.e)("Created by"),Cell:({row:{original:{created_by:e}}})=>e?`${e.first_name} ${e.last_name}`:"",size:"xl"},{Cell:({row:{original:e}})=>{var t;const a=s()(t=[B?{label:"edit-action",tooltip:Object(r.e)("Edit template"),placement:"bottom",icon:"Edit",onClick:()=>(H(e),void D(!0))}:null,E?{label:"delete-action",tooltip:Object(r.e)("Delete template"),placement:"bottom",icon:"Trash",onClick:()=>z(e)}:null]).call(t,e=>!!e);return Object(k.jsx)(S.a,{actions:a})},Header:Object(r.e)("Actions"),id:"actions",disableSortBy:!0,hidden:!B&&!E,size:"xl"}],[E,A]),q={name:Object(r.e)("CSS templates")},L=[];A&&L.push({name:Object(k.jsx)(i.a.Fragment,null,Object(k.jsx)("i",{className:"fa fa-plus"})," ",Object(r.e)("CSS template")),buttonStyle:"primary",onClick:()=>{H(null),D(!0)}}),E&&L.push({name:Object(r.e)("Bulk select"),onClick:v,buttonStyle:"secondary"}),q.buttons=L;const R=Object(o.useMemo)(()=>[{Header:Object(r.e)("Created by"),id:"created_by",input:"select",operator:y.a.relationOneMany,unfilteredLabel:"All",fetchSelects:Object(O.g)("css_template","created_by",Object(O.e)(e=>Object(r.e)("An error occurred while fetching dataset datasource values: %s",e)),a.userId),paginate:!0},{Header:Object(r.e)("Search"),id:"template_name",input:"search",operator:y.a.contains}],[]);return Object(k.jsx)(i.a.Fragment,null,Object(k.jsx)(g.a,q),Object(k.jsx)(N,{addDangerToast:e,cssTemplate:T,onCssTemplateAdd:()=>C(),onHide:()=>D(!1),show:$}),U&&Object(k.jsx)(x.a,{description:Object(r.e)("This action will permanently delete the template."),onConfirm:()=>{U&&(({id:a,template_name:l})=>{d.a.delete({endpoint:`/api/v1/css_template/${a}`}).then(()=>{C(),z(null),t(Object(r.e)("Deleted: %s",l))},Object(O.e)(t=>e(Object(r.e)("There was an issue deleting %s: %s",l,t))))})(U)},onHide:()=>z(null),open:!0,title:Object(r.e)("Delete Template?")}),Object(k.jsx)(f.a,{title:Object(r.e)("Please confirm"),description:Object(r.e)("Are you sure you want to delete the selected templates?"),onConfirm:a=>{d.a.delete({endpoint:`/api/v1/css_template/?q=${m.a.encode(c()(a).call(a,({id:e})=>e))}`}).then(({json:e={}})=>{C(),t(e.message)},Object(O.e)(t=>e(Object(r.e)("There was an issue deleting the selected templates: %s",t))))}},e=>{const t=E?[{key:"delete",name:Object(r.e)("Delete"),onSelect:e,type:"danger"}]:[];return Object(k.jsx)(y.b,{className:"css-templates-list-view",columns:P,count:n,data:b,fetchData:w,filters:R,initialSort:M,loading:l,pageSize:25,bulkActions:t,bulkSelectEnabled:u,disableBulkSelect:v})}))}))}}]);