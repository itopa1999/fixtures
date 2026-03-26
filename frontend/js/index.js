/* ========================================
   DASHBOARD DATA POPULATION
   ======================================== */

(function() {
    // Stats
    document.getElementById('totalTournaments').innerText = '18';
    document.getElementById('activeTournaments').innerText = '3';
    document.getElementById('totalPlayers').innerText = '142';
    document.getElementById('totalMatches').innerText = '327';

    // Active Tournaments
    const activeContainer = document.getElementById('activeTournamentsContainer');
    if (activeContainer) {
        activeContainer.innerHTML = `
            <div class="card tournament-card">
                <span class="tournament-status status-active">Active</span>
                <div class="card-header"><div class="card-icon">🏆</div><div><div class="card-title">Mortal Kombat Championship</div><div class="card-subtitle">Single Elimination</div></div></div>
                <div class="card-body">
                    <div class="tournament-info-row"><span class="info-label">Players:</span><span class="info-value">24 / 32</span></div>
                    <div class="tournament-info-row"><span class="info-label">Round:</span><span class="info-value">Semi-Finals</span></div>
                    <div class="tournament-info-row"><span class="info-label">Matches Today:</span><span class="info-value">4 / 4</span></div>
                </div>
                <div class="card-footer"><span>Started 2h ago</span><span class="badge badge-primary">Details</span></div>
            </div>
            <div class="card tournament-card">
                <span class="tournament-status status-registration">Registration</span>
                <div class="card-header"><div class="card-icon">👾</div><div><div class="card-title">Street Fighter 6 Cup</div><div class="card-subtitle">Group Stage + KO</div></div></div>
                <div class="card-body">
                    <div class="tournament-info-row"><span class="info-label">Players:</span><span class="info-value">18 / 24</span></div>
                    <div class="tournament-info-row"><span class="info-label">Groups:</span><span class="info-value">6 groups</span></div>
                    <div class="tournament-info-row"><span class="info-label">Start in:</span><span class="info-value">3 days</span></div>
                </div>
                <div class="card-footer"><span>Created 5d ago</span><span class="badge badge-warning">Manage</span></div>
            </div>
            <div class="card tournament-card">
                <span class="tournament-status status-active">Active</span>
                <div class="card-header"><div class="card-icon">🎯</div><div><div class="card-title">Double Elimination Qualifier</div><div class="card-subtitle">Double Elimination</div></div></div>
                <div class="card-body">
                    <div class="tournament-info-row"><span class="info-label">Players:</span><span class="info-value">16 / 16</span></div>
                    <div class="tournament-info-row"><span class="info-label">Phase:</span><span class="info-value">Winners R2</span></div>
                    <div class="tournament-info-row"><span class="info-label">Completion:</span><span class="info-value">40%</span></div>
                </div>
                <div class="card-footer"><span>Started 1d ago</span><span class="badge badge-success">In Progress</span></div>
            </div>
        `;
    }

    // Matches
    const matchesBody = document.getElementById('matchesBody');
    if (matchesBody) {
        matchesBody.innerHTML = `
            <tr><td><strong>MK Champ</strong></td><td>SonicFox</td><td>2 - 1</td><td>Dragon</td><td>Semi-Finals</td><td><span class="badge badge-success">Completed</span></td></tr>
            <tr><td><strong>MK Champ</strong></td><td>Rewind</td><td>1 - 2</td><td>Kombat</td><td>Semi-Finals</td><td><span class="badge badge-success">Completed</span></td></tr>
            <tr><td><strong>Double Elim</strong></td><td>Champion</td><td>2 - 0</td><td>Challenger</td><td>Winners R2</td><td><span class="badge badge-success">Completed</span></td></tr>
            <tr><td><strong>Double Elim</strong></td><td>Fighter42</td><td>0 - 0</td><td>Warrior</td><td>Winners R2</td><td><span class="badge badge-primary">Scheduled</span></td></tr>
            <tr><td><strong>SF6 Cup</strong></td><td>-</td><td>-</td><td>-</td><td>Group A</td><td><span class="badge badge-warning">Pending</span></td></tr>
        `;
    }
})();
