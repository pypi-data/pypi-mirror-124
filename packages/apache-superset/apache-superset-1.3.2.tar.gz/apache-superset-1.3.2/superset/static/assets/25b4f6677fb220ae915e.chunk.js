(window.webpackJsonp=window.webpackJsonp||[]).push([[24],{4681:function(t,e,n){"use strict";n.d(e,"a",(function(){return b}));var a=n(11),o=n.n(a),s=(n(0),n(40)),c=n(51),l=n(31),i=n(1);const r=s.g.span`
  white-space: nowrap;
  min-width: 100px;
  svg,
  i {
    margin-right: 8px;

    &:hover {
      path {
        fill: ${({theme:t})=>t.colors.primary.base};
      }
    }
  }
`,d=s.g.span`
  color: ${({theme:t})=>t.colors.grayscale.base};
`;function b({actions:t}){return Object(i.jsx)(r,{className:"actions"},o()(t).call(t,(t,e)=>{const n=l.a[t.icon];return t.tooltip?Object(i.jsx)(c.a,{id:`${t.label}-tooltip`,title:t.tooltip,placement:t.placement,key:e},Object(i.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:t.onClick},Object(i.jsx)(n,null))):Object(i.jsx)(d,{role:"button",tabIndex:0,className:"action-button",onClick:t.onClick,key:e},Object(i.jsx)(n,null))}))}},5072:function(t,e,n){"use strict";n.r(e);n(41);var a=n(11),o=n.n(a),s=n(0),c=n.n(s),l=n(365),i=n(349),r=n(13),d=n(66),b=n(40),j=n(37),u=n.n(j),m=n(111),O=n.n(m),h=n(4681),x=n(45),p=n(1584),g=n(961),_=n(4669),f=n(720),y=n(65),w=n(142),v=n(418),k=n(117),$=n(706),S=n(31),C=n(114),D=n(310),A=n(1);const H=b.g.div`
  margin: ${({theme:t})=>2*t.gridUnit}px auto
    ${({theme:t})=>4*t.gridUnit}px auto;
`,N=Object(b.g)(D.d)`
  border-radius: ${({theme:t})=>t.borderRadius}px;
  border: 1px solid ${({theme:t})=>t.colors.secondary.light2};
`,T=b.g.div`
  margin-bottom: ${({theme:t})=>5*t.gridUnit}px;

  .control-label {
    margin-bottom: ${({theme:t})=>2*t.gridUnit}px;
  }

  .required {
    margin-left: ${({theme:t})=>t.gridUnit/2}px;
    color: ${({theme:t})=>t.colors.error.base};
  }

  textarea {
    flex: 1 1 auto;
    height: ${({theme:t})=>17*t.gridUnit}px;
    resize: none;
    width: 100%;
  }

  textarea,
  input[type='text'] {
    padding: ${({theme:t})=>1.5*t.gridUnit}px
      ${({theme:t})=>2*t.gridUnit}px;
    border: 1px solid ${({theme:t})=>t.colors.grayscale.light2};
    border-radius: ${({theme:t})=>t.gridUnit}px;
  }

  input[type='text'] {
    width: 65%;
  }
`;var Y=Object(w.a)(({addDangerToast:t,addSuccessToast:e,annnotationLayerId:n,annotation:a=null,onAnnotationAdd:o,onHide:c,show:l})=>{var i,d;const[b,j]=Object(s.useState)(!0),[m,O]=Object(s.useState)(null),h=null!==a,{state:{loading:x,resource:p},fetchResource:g,createResource:_,updateResource:f}=Object(v.l)(`annotation_layer/${n}/annotation`,Object(r.e)("annotation"),t),y=()=>{O({short_descr:"",start_dttm:"",end_dttm:"",json_metadata:"",long_descr:""})},w=()=>{h?O(p):y(),c()},D=t=>{const{target:e}=t,n={...m,end_dttm:m?m.end_dttm:"",short_descr:m?m.short_descr:"",start_dttm:m?m.start_dttm:""};n[e.name]=e.value,O(n)};return Object(s.useEffect)(()=>{if(h&&(!m||!m.id||a&&a.id!==m.id||l)){if(a&&null!==a.id&&!x){const t=a.id||0;g(t)}}else h||m&&!m.id&&!l||y()},[a]),Object(s.useEffect)(()=>{p&&O(p)},[p]),Object(s.useEffect)(()=>{m&&m.short_descr.length&&m.start_dttm.length&&m.end_dttm.length?j(!1):j(!0)},[m?m.short_descr:"",m?m.start_dttm:"",m?m.end_dttm:""]),Object(A.jsx)(C.b,{disablePrimaryButton:b,onHandledPrimaryAction:()=>{if(h){if(m&&m.id){const t=m.id;delete m.id,delete m.created_by,delete m.changed_by,delete m.changed_on_delta_humanized,delete m.layer,f(t,m).then(t=>{t&&(o&&o(),w(),e(Object(r.e)("The annotation has been updated")))})}}else m&&_(m).then(t=>{t&&(o&&o(),w(),e(Object(r.e)("The annotation has been saved")))})},onHide:w,primaryButtonName:h?Object(r.e)("Save"):Object(r.e)("Add"),show:l,width:"55%",title:Object(A.jsx)("h4",null,h?Object(A.jsx)(S.a.EditAlt,{css:k.d}):Object(A.jsx)(S.a.PlusLarge,{css:k.d}),h?Object(r.e)("Edit annotation"):Object(r.e)("Add annotation"))},Object(A.jsx)(H,null,Object(A.jsx)("h4",null,Object(r.e)("Basic information"))),Object(A.jsx)(T,null,Object(A.jsx)("div",{className:"control-label"},Object(r.e)("Annotation name"),Object(A.jsx)("span",{className:"required"},"*")),Object(A.jsx)("input",{name:"short_descr",onChange:D,type:"text",value:null==m?void 0:m.short_descr})),Object(A.jsx)(T,null,Object(A.jsx)("div",{className:"control-label"},Object(r.e)("date"),Object(A.jsx)("span",{className:"required"},"*")),Object(A.jsx)($.b,{format:"YYYY-MM-DD HH:mm",onChange:(t,e)=>{const n={...m,end_dttm:m&&e[1].length?u()(e[1]).format("YYYY-MM-DD HH:mm"):"",short_descr:m?m.short_descr:"",start_dttm:m&&e[0].length?u()(e[0]).format("YYYY-MM-DD HH:mm"):""};O(n)},showTime:{format:"hh:mm a"},use12Hours:!0,value:null!=m&&null!=(i=m.start_dttm)&&i.length||null!=m&&null!=(d=m.end_dttm)&&d.length?[u()(m.start_dttm),u()(m.end_dttm)]:null})),Object(A.jsx)(H,null,Object(A.jsx)("h4",null,Object(r.e)("Additional information"))),Object(A.jsx)(T,null,Object(A.jsx)("div",{className:"control-label"},Object(r.e)("description")),Object(A.jsx)("textarea",{name:"long_descr",value:m?m.long_descr:"",placeholder:Object(r.e)("Description (this can be seen in the list)"),onChange:D})),Object(A.jsx)(T,null,Object(A.jsx)("div",{className:"control-label"},Object(r.e)("JSON metadata")),Object(A.jsx)(N,{onChange:t=>{const e={...m,end_dttm:m?m.end_dttm:"",json_metadata:t,short_descr:m?m.short_descr:"",start_dttm:m?m.start_dttm:""};O(e)},value:m&&m.json_metadata?m.json_metadata:"",width:"100%",height:"120px"})))});e.default=Object(w.a)((function({addDangerToast:t,addSuccessToast:e}){const{annotationLayerId:n}=Object(l.g)(),{state:{loading:a,resourceCount:j,resourceCollection:m,bulkSelectEnabled:w},fetchData:$,refreshData:S,toggleBulkSelect:C}=Object(v.k)(`annotation_layer/${n}/annotation`,Object(r.e)("annotation"),t,!1),[D,H]=Object(s.useState)(!1),[N,T]=Object(s.useState)(""),[E,B]=Object(s.useState)(null),[U,L]=Object(s.useState)(null),M=t=>{B(t),H(!0)},I=Object(s.useCallback)((async function(){try{const t=await d.a.get({endpoint:`/api/v1/annotation_layer/${n}`});T(t.json.result.name)}catch(e){await Object(y.a)(e).then(({error:e})=>{t(e.error||e.statusText||e)})}}),[n]);Object(s.useEffect)(()=>{I()},[I]);const q=[{id:"short_descr",desc:!0}],z=Object(s.useMemo)(()=>[{accessor:"short_descr",Header:Object(r.e)("Label")},{accessor:"long_descr",Header:Object(r.e)("Description")},{Cell:({row:{original:{start_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:Object(r.e)("Start"),accessor:"start_dttm"},{Cell:({row:{original:{end_dttm:t}}})=>u()(new Date(t)).format("ll"),Header:Object(r.e)("End"),accessor:"end_dttm"},{Cell:({row:{original:t}})=>{const e=[{label:"edit-action",tooltip:Object(r.e)("Edit annotation"),placement:"bottom",icon:"Edit",onClick:()=>M(t)},{label:"delete-action",tooltip:Object(r.e)("Delete annotation"),placement:"bottom",icon:"Trash",onClick:()=>L(t)}];return Object(A.jsx)(h.a,{actions:e})},Header:Object(r.e)("Actions"),id:"actions",disableSortBy:!0}],[!0,!0]),P=[];P.push({name:Object(A.jsx)(c.a.Fragment,null,Object(A.jsx)("i",{className:"fa fa-plus"})," ",Object(r.e)("Annotation")),buttonStyle:"primary",onClick:()=>{M(null)}}),P.push({name:Object(r.e)("Bulk select"),onClick:C,buttonStyle:"secondary","data-test":"annotation-bulk-select"});const R=b.g.div`
    display: flex;
    flex-direction: row;

    a,
    Link {
      margin-left: 16px;
      font-size: 12px;
      font-weight: normal;
      text-decoration: underline;
    }
  `;let F=!0;try{Object(l.f)()}catch(t){F=!1}const J=Object(A.jsx)(x.a,{buttonStyle:"primary",onClick:()=>{M(null)}},Object(A.jsx)(c.a.Fragment,null,Object(A.jsx)("i",{className:"fa fa-plus"})," ",Object(r.e)("Annotation"))),G={message:Object(r.e)("No annotation yet"),slot:J};return Object(A.jsx)(c.a.Fragment,null,Object(A.jsx)(f.a,{name:Object(A.jsx)(R,null,Object(A.jsx)("span",null,Object(r.e)(`Annotation Layer ${N}`)),Object(A.jsx)("span",null,F?Object(A.jsx)(i.b,{to:"/annotationlayermodelview/list/"},"Back to all"):Object(A.jsx)("a",{href:"/annotationlayermodelview/list/"},"Back to all"))),buttons:P}),Object(A.jsx)(Y,{addDangerToast:t,addSuccessToast:e,annotation:E,show:D,onAnnotationAdd:()=>S(),annnotationLayerId:n,onHide:()=>H(!1)}),U&&Object(A.jsx)(g.a,{description:Object(r.e)(`Are you sure you want to delete ${null==U?void 0:U.short_descr}?`),onConfirm:()=>{U&&(({id:a,short_descr:o})=>{d.a.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/${a}`}).then(()=>{S(),L(null),e(Object(r.e)("Deleted: %s",o))},Object(k.e)(e=>t(Object(r.e)("There was an issue deleting %s: %s",o,e))))})(U)},onHide:()=>L(null),open:!0,title:Object(r.e)("Delete Annotation?")}),Object(A.jsx)(p.a,{title:Object(r.e)("Please confirm"),description:Object(r.e)("Are you sure you want to delete the selected annotations?"),onConfirm:a=>{d.a.delete({endpoint:`/api/v1/annotation_layer/${n}/annotation/?q=${O.a.encode(o()(a).call(a,({id:t})=>t))}`}).then(({json:t={}})=>{S(),e(t.message)},Object(k.e)(e=>t(Object(r.e)("There was an issue deleting the selected annotations: %s",e))))}},t=>{const e=[{key:"delete",name:Object(r.e)("Delete"),onSelect:t,type:"danger"}];return Object(A.jsx)(_.b,{className:"annotations-list-view",bulkActions:e,bulkSelectEnabled:w,columns:z,count:j,data:m,disableBulkSelect:C,emptyState:G,fetchData:$,initialSort:q,loading:a,pageSize:25})}))}))}}]);