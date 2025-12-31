from typing import List, Optional
import os
import pandas as pd
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from ..database import get_session
from ..models import User, ChatSession, Message, File
from ..dependencies import get_current_user
from ..agent_factory import get_agent

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    file_id: int

class ChatResponse(BaseModel):
    response: str
    session_id: int

@router.post("/sessions", response_model=ChatSession)
def create_session(
    file_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    # Verify file ownership
    file = session.get(File, file_id)
    if not file or file.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="File not found")

    chat_session = ChatSession(user_id=current_user.id, file_id=file_id, title=f"Chat about {file.filename}")
    session.add(chat_session)
    session.commit()
    session.refresh(chat_session)
    return chat_session

@router.get("/sessions", response_model=List[ChatSession])
def list_sessions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    statement = select(ChatSession).where(ChatSession.user_id == current_user.id)
    return session.exec(statement).all()

@router.get("/history/{session_id}", response_model=List[Message])
def get_history(
    session_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    chat_session = session.get(ChatSession, session_id)
    if not chat_session or chat_session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
        
    return chat_session.messages

@router.post("/message/{session_id}")
def send_message(
    session_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_session)
):
    chat_session = db_session.get(ChatSession, session_id)
    if not chat_session or chat_session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    file = db_session.get(File, chat_session.file_id)
    if not file:
         raise HTTPException(status_code=404, detail="File associated with chat not found")

    # Check if file exists on disk
    if not os.path.exists(file.filepath):
        raise HTTPException(
            status_code=404, 
            detail=f"File '{file.filename}' not found on disk. Please re-upload the file."
        )

    # Save User Message
    user_msg = Message(content=request.message, role="user", session_id=session_id)
    db_session.add(user_msg)
    db_session.commit()

    # Invoke Agent
    try:
        if file.filename.endswith((".csv", ".xlsx", ".xls")):
            agent = get_agent(file.filepath)
            response_text = agent.invoke(request.message)["output"]
        else:
            # RAG flow
            from ..rag_pipeline import RagPipeline
            rag = RagPipeline(file.filepath, str(file.id))
            chain = rag.get_chain()
            res = chain.invoke(request.message)
            response_text = res["result"]
            
            # Append citations if available
            if res.get("source_documents"):
                response_text += "\n\n**Sources:**\n"
                for doc in res["source_documents"]:
                    page = doc.metadata.get("page", "N/A")
                    src = doc.metadata.get("source", "N/A")
                    response_text += f"- Page {page} ({src})\n"

    except Exception as e:
        response_text = f"Error processing request: {str(e)}"

    # Save Assistant Message
    assistant_msg = Message(content=response_text, role="assistant", session_id=session_id)
    db_session.add(assistant_msg)
    db_session.commit()
    
    return {"response": response_text}

@router.post("/build-dashboard")
def build_dashboard(
    current_user: User = Depends(get_current_user),
    db_session: Session = Depends(get_session)
):
    """Analyze all user files and build an intelligent dashboard"""
    
    # Get all user files
    statement = select(File).where(File.owner_id == current_user.id)
    files = db_session.exec(statement).all()
    
    if not files:
        raise HTTPException(status_code=404, detail="No files found. Please upload data first.")
    
    dashboard_data = {
        "summary": {},
        "charts": [],
        "insights": [],
        "kpis": []
    }
    
    try:
        # Analyze each CSV/Excel file
        for file in files:
            if not os.path.exists(file.filepath):
                continue
                
            if file.filepath.endswith(('.csv', '.xlsx', '.xls')):
                try:
                    # Read data
                    if file.filepath.endswith('.csv'):
                        df = pd.read_csv(file.filepath)
                    else:
                        df = pd.read_excel(file.filepath)
                    
                    # Basic statistics
                    file_stats = {
                        "filename": file.filename,
                        "rows": len(df),
                        "columns": len(df.columns),
                        "numeric_cols": df.select_dtypes(include=['number']).columns.tolist(),
                        "categorical_cols": df.select_dtypes(include=['object']).columns.tolist(),
                    }
                    
                    # Generate KPIs
                    kpis = []
                    for col in df.select_dtypes(include=['number']).columns[:4]:
                        kpis.append({
                            "title": f"Total {col}",
                            "value": float(df[col].sum()),
                            "format": "number"
                        })
                        kpis.append({
                            "title": f"Avg {col}",
                            "value": float(df[col].mean()),
                            "format": "decimal"
                        })
                    
                    # Suggest charts
                    charts = []
                    
                    # Bar chart for categorical vs numeric
                    if len(file_stats['categorical_cols']) > 0 and len(file_stats['numeric_cols']) > 0:
                        cat_col = file_stats['categorical_cols'][0]
                        num_col = file_stats['numeric_cols'][0]
                        
                        if len(df[cat_col].unique()) <= 20:
                            # Generate matplotlib plot
                            import matplotlib.pyplot as plt
                            import seaborn as sns
                            import uuid
                            
                            plt.figure(figsize=(10, 6))
                            chart_data = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(10)
                            
                            colors = sns.color_palette("viridis", len(chart_data))
                            bars = plt.bar(range(len(chart_data)), chart_data.values, color=colors)
                            plt.xticks(range(len(chart_data)), chart_data.index, rotation=45, ha='right')
                            plt.xlabel(cat_col, fontsize=12, fontweight='bold')
                            plt.ylabel(num_col, fontsize=12, fontweight='bold')
                            plt.title(f"{num_col} by {cat_col}", fontsize=14, fontweight='bold', pad=20)
                            plt.tight_layout()
                            
                            # Add value labels on bars
                            for bar in bars:
                                height = bar.get_height()
                                plt.text(bar.get_x() + bar.get_width()/2., height,
                                        f'{height:,.0f}',
                                        ha='center', va='bottom', fontsize=9)
                            
                            plot_id = str(uuid.uuid4())
                            plot_path = f"static/plots/{plot_id}.png"
                            plt.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='white')
                            plt.close()
                            
                            charts.append({
                                "type": "bar",
                                "title": f"{num_col} by {cat_col}",
                                "image": f"http://localhost:8000/{plot_path}",
                                "xLabel": cat_col,
                                "yLabel": num_col
                            })
                    
                    # Pie chart for categorical distribution
                    if len(file_stats['categorical_cols']) > 0:
                        cat_col = file_stats['categorical_cols'][0]
                        if len(df[cat_col].unique()) <= 10:
                            import matplotlib.pyplot as plt
                            import uuid
                            
                            plt.figure(figsize=(8, 8))
                            dist = df[cat_col].value_counts().head(8)
                            
                            colors = plt.cm.Set3(range(len(dist)))
                            plt.pie(dist.values, labels=dist.index, autopct='%1.1f%%', 
                                   startangle=90, colors=colors, textprops={'fontsize': 10})
                            plt.title(f"Distribution of {cat_col}", fontsize=14, fontweight='bold', pad=20)
                            plt.axis('equal')
                            
                            plot_id = str(uuid.uuid4())
                            plot_path = f"static/plots/{plot_id}.png"
                            plt.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='white')
                            plt.close()
                            
                            charts.append({
                                "type": "pie",
                                "title": f"Distribution of {cat_col}",
                                "image": f"http://localhost:8000/{plot_path}"
                            })
                    
                    # Line chart for trends (if numeric data)
                    if len(file_stats['numeric_cols']) >= 1:
                        import matplotlib.pyplot as plt
                        import seaborn as sns
                        import uuid
                        
                        plt.figure(figsize=(12, 6))
                        
                        for idx, col in enumerate(file_stats['numeric_cols'][:3]):
                            plt.plot(df[col].head(50).values, marker='o', linewidth=2, 
                                   markersize=4, label=col)
                        
                        plt.xlabel("Index", fontsize=12, fontweight='bold')
                        plt.ylabel("Value", fontsize=12, fontweight='bold')
                        plt.title("Trend Analysis", fontsize=14, fontweight='bold', pad=20)
                        plt.legend(loc='best', fontsize=10)
                        plt.grid(True, alpha=0.3)
                        plt.tight_layout()
                        
                        plot_id = str(uuid.uuid4())
                        plot_path = f"static/plots/{plot_id}.png"
                        plt.savefig(plot_path, dpi=150, bbox_inches='tight', facecolor='white')
                        plt.close()
                        
                        charts.append({
                            "type": "line",
                            "title": "Trend Analysis",
                            "image": f"http://localhost:8000/{plot_path}"
                        })
                    
                    dashboard_data["charts"].extend(charts[:6])  # Max 6 charts per file
                    dashboard_data["kpis"].extend(kpis[:6])  # Max 6 KPIs per file
                    
                    # Generate statistical insights (no LLM needed)
                    insights_text = f"📊 **Data Summary for {file.filename}**\n\n"
                    insights_text += f"• Total records: {len(df):,}\n"
                    insights_text += f"• Number of columns: {len(df.columns)}\n"
                    
                    # Numeric insights
                    for col in file_stats['numeric_cols'][:3]:
                        insights_text += f"• {col}: Min={df[col].min():,.2f}, Max={df[col].max():,.2f}, Avg={df[col].mean():,.2f}\n"
                    
                    # Categorical insights
                    for col in file_stats['categorical_cols'][:2]:
                        top_val = df[col].value_counts().head(1)
                        if len(top_val) > 0:
                            insights_text += f"• Top {col}: {top_val.index[0]} ({top_val.values[0]:,} records)\n"
                    
                    dashboard_data["insights"].append({
                        "file": file.filename,
                        "text": insights_text
                    })
                    
                except Exception as e:
                    print(f"Error analyzing {file.filename}: {str(e)}")
                    continue
        
        # Calculate summary totals
        total_rows = 0
        for file_obj in files:
            if file_obj.filepath.endswith(('.csv', '.xlsx', '.xls')) and os.path.exists(file_obj.filepath):
                try:
                    if file_obj.filepath.endswith('.csv'):
                        df = pd.read_csv(file_obj.filepath)
                    else:
                        df = pd.read_excel(file_obj.filepath)
                    total_rows += len(df)
                except:
                    pass
        
        dashboard_data["summary"] = {
            "total_files": len(files),
            "total_rows": total_rows,
            "charts_count": len(dashboard_data["charts"]),
            "insights_count": len(dashboard_data["insights"])
        }
        
        return dashboard_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building dashboard: {str(e)}")
