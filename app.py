import csv
import io
import streamlit as st
from model import BUDGET, SEGMENTS, RESPONSES, calculate, totals

st.set_page_config(page_title='STP Decision Lab', page_icon='👟', layout='wide')
st.markdown('''<style>.block-container{max-width:1120px;padding-top:2rem}h1,h2,h3{color:#10233f}.stButton button{border-radius:8px}.note{padding:1rem;background:#e8f5ef;border-left:5px solid #1e7051;border-radius:5px}.card{padding:1rem;background:#eaf3f7;border-radius:8px;min-height:175px;margin-bottom:.7rem}</style>''', unsafe_allow_html=True)
if 'round' not in st.session_state: st.session_state.round=1
if 'baseline' not in st.session_state: st.session_state.baseline=None
def reset():
    for key in list(st.session_state): del st.session_state[key]
def go(n): st.session_state.round=n
with st.sidebar:
    st.markdown('### Whittier Interactive Learning Labs')
    st.caption('BSAD 350 · International Business')
    mode=st.radio('Choose a lab', ['Monday · Stride practice','Wednesday · Project workspace'])
    st.button('Reset this session',on_click=reset,help='Clears both lab modes in this browser session.')
    st.caption('Work is private to this browser session and may be lost on refresh, disconnect or reset. Download your summary before leaving. No student account is needed.')

st.title('STP Decision Lab')
st.markdown('<div class="note"><strong>Fictional teaching model:</strong> Stride, all segment sizes, prices, costs, behavioral relationships and competitive events are invented. They are not German market data or forecasts. Results support discussion, not a guaranteed right answer.</div>',unsafe_allow_html=True)

if mode.startswith('Monday'):
    st.write('**Monday, October 19, 2026 · 3:00–4:20 p.m.** Work in pairs for about 20 minutes. You lead Stride, a fictional US footwear company entering Germany. Discuss the evidence you would need before making a real commitment.')
    st.caption('Four rounds: Explore 4 min · Choose 5 min · Test 5 min · Respond & compare 6 min. The remaining class time is available for discussion and other activities.')
    n=st.session_state.round
    st.progress((n-1)/4,text=f'Round {n} of 4')
    if n==1:
        st.header('1 · Explore the segments')
        st.write('Compare the fictional segment profiles. What needs distinguish them? Which might Stride serve credibly?')
        cols=st.columns(2)
        descriptions=['Wants running performance and is willing to pay for it.','Values environmental positioning; claims would need evidence.','Prioritizes versatile comfort for everyday use.','Looks for accessible prices; price-sensitive in this model.']
        for i,((name,s),desc) in enumerate(zip(SEGMENTS.items(),descriptions)):
            cols[i%2].markdown(f'<div class="card"><h3>{s["icon"]} {name}</h3>{desc}<br><br>Fictional potential buyers: {s["buyers"]:,}<br>Reference price: ${s["reference"]}</div>',unsafe_allow_html=True)
        st.button('Continue to targeting',on_click=go,args=(2,),type='primary')
    if n>=2:
        if n==2: st.header('2 · Choose your target and position')
        elif n==3: st.header('3 · Allocate and test')
        else: st.header('4 · Respond to a competitor')
        if n==4:
            st.warning('A fictional competitor launches a discount aimed at everyday comfort and budget students. In this model their demand falls 25% before your response. Other segments are unaffected.')
        st.write('Select one or more targets, one positioning promise, a common selling price and a marketing allocation for each target. Allocations may total less than $200,000; unspent money is not a cost.')
        targets=st.multiselect('Target segments',list(SEGMENTS),default=['Everyday comfort'],key='targets')
        position=st.selectbox('Positioning promise',['Performance','Sustainability','Comfort','Value'],key='position')
        price=st.slider('Selling price per pair ($)',50,200,110,5,key='price')
        allocations={}
        for name in targets:
            allocations[name]=st.number_input(f'Marketing allocation · {name} ($)',min_value=0,max_value=BUDGET,value=50000,step=5000,key='allocation_'+name)
        spend=sum(allocations.values())
        st.write(f'Allocated: **${spend:,.0f}** of $200,000 · Remaining: **${BUDGET-spend:,.0f}**')
        response=st.selectbox('Competitive response',list(RESPONSES),key='response') if n==4 else 'Hold course'
        if n==4: st.caption('For affected segments only: match promotion raises demand 15% but costs $10 per pair; differentiation raises demand 8% but costs $4 per pair; hold has no extra effect. These are assumptions, not guarantees.')
        if not targets or spend>BUDGET:
            st.error('Select at least one segment and keep allocations at or below $200,000.')
        else:
            rows=calculate(targets,position,price,allocations,n==4,response); t=totals(rows)
            st.subheader('Live estimates')
            a,b,c=st.columns(3); a.metric('Pairs sold',f'{t["units"]:,}'); b.metric('Revenue',f'${t["revenue"]:,.0f}'); c.metric('Contribution after marketing',f'${t["contribution"]:,.0f}')
            st.caption('Contribution subtracts fictional $65 variable cost per pair, any response cost, and marketing. It is not net profit: fixed costs, taxes, distribution, and currency effects are excluded. Negative contribution is possible.')
            st.dataframe([{'Segment':r['segment'],'Marketing':r['spend'],'Pairs':r['units'],'Revenue':r['revenue'],'Contribution':r['contribution']} for r in rows],hide_index=True,use_container_width=True)
            if n==2: st.button('Continue to testing',on_click=go,args=(3,),type='primary')
            if n==3:
                st.info('Try a different price or allocation. How does additional reach compare with the marketing cost? Which segment-position fit is strongest?')
                if st.button('Save strategy and reveal challenge',type='primary'):
                    st.session_state.baseline={'targets':list(targets),'position':position,'price':price,'allocations':dict(allocations),'totals':t.copy()}; go(4); st.rerun()
            if n==4 and st.session_state.baseline:
                base=st.session_state.baseline
                st.subheader('Before and after the challenge')
                st.table([{'Measure':k.title(),'Saved before event':base['totals'][k],'Current after event':t[k]} for k in ('units','revenue','contribution','spend')])
                st.caption('The comparison includes both the competitor event and any changes you make to strategy; it does not isolate their individual effects.')
                reason=st.text_area('Pair reflection: Why this strategy? What trade-off and uncertainty matter most?',key='reason')
                summary=f'''STP DECISION LAB — PAIR SUMMARY\nAll figures are fictional teaching assumptions.\n\nBefore challenge: {base['targets']}; {base['position']}; price ${base['price']}; allocation {base['allocations']}; results {base['totals']}\nAfter challenge: {targets}; {position}; price ${price}; allocation {allocations}; response {response}; results {t}\n\nOur reasoning and uncertainty: {reason}\nContribution is not net profit.\n'''
                st.download_button('Download pair summary',summary,'stride-summary.txt','text/plain')
                st.text_area('Copyable pair summary',summary,height=180)
                st.write('**Debrief:** What did you change, why, and what real evidence might overturn your decision?')
        if n>1: st.button('Back',on_click=go,args=(n-1,))
    with st.expander('See the formulas and assumptions'):
        st.markdown('''For each selected segment: **pairs = round(potential buyers × 12% base conversion × reach × positioning fit × price factor × competitor factor × response factor)**. Reach = marketing / (marketing + $50,000), or zero with no marketing. Price factor = 1 − elasticity × (price − reference price) / reference price, bounded between 0.25 and 1.50. Revenue = pairs × price. Contribution = pairs × (price − $65 − response cost) − marketing. The competitor factor is 0.75 for affected segments after the event and 1 otherwise. Round each segment before totaling. All coefficients are invented. Raising price increases unit margin but generally reduces demand; additional marketing has diminishing returns.''')
        st.dataframe([{'Segment':k,'Potential buyers':v['buyers'],'Reference price':v['reference'],'Price sensitivity':v['elasticity'],**v['fit']} for k,v in SEGMENTS.items()],hide_index=True,use_container_width=True)
else:
    st.header('Wednesday · Project workspace')
    st.info('A simple planning workspace, not a validated market forecast. Enter your own sources and assumptions; no market data are supplied. Compare the same measurement period and currency across markets.')
    company=st.text_input('Company and product',key='company')
    markets=[]
    for i in range(1,4):
        with st.expander(f'Market {i}',expanded=True):
            name=st.text_input('Country / market',key=f'market{i}')
            segment=st.text_input('Target segment and positioning',key=f'segment{i}')
            population=st.number_input('Potential buyers in target segment',min_value=0,step=1000,key=f'population{i}')
            rate=st.number_input('Assumed share captured (%)',min_value=0.0,max_value=100.0,step=0.1,key=f'rate{i}')
            price=st.number_input('Price per unit (same currency across markets)',min_value=0.0,step=1.0,key=f'project_price{i}')
            source=st.text_area('Sources, dates, units and reasoning for assumptions',key=f'source{i}')
            units=population*rate/100; revenue=units*price
            st.write(f'Illustrative units: **{units:,.1f}** · revenue: **{revenue:,.2f}** (your chosen currency)')
            markets.append(dict(market=name,segment=segment,potential_buyers=population,share_percent=rate,price=price,units=units,revenue=revenue,sources=source))
    note=st.text_area('Comparison, limitations, and next research steps',key='project_note')
    st.caption('Units = potential buyers × assumed captured share. Revenue = units × price. These are user-entered scenarios, not verified data; do not double-count buyers or mix periods. Costs, capacity and exchange rates are not modeled.')
    text=f'PROJECT STP WORKSPACE\nCompany/product: {company}\n'+'\n'.join(str(m) for m in markets)+f'\nComparison and next steps: {note}\n'
    st.text_area('Copy to Miro',text,height=200)
    st.download_button('Download project summary',text,'project-summary.txt','text/plain')
    buf=io.StringIO(); writer=csv.DictWriter(buf,fieldnames=list(markets[0])); writer.writeheader(); writer.writerows(markets)
    st.download_button('Download market assumptions CSV',buf.getvalue(),'market-assumptions.csv','text/csv')
