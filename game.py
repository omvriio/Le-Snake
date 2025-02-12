import streamlit as st
import streamlit.components.v1 as components

# Define the HTML and JavaScript for the game
game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Moroccan-Themed 1v1 Snake Game</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #FFD700; /* Moroccan gold */
            font-family: 'Arial', sans-serif;
            overflow: hidden;
        }
        canvas {
            border: 5px solid #004411; /* Moroccan green */
            background-color: #FFF8DC; /* Moroccan cream */
        }
        .score-container {
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        .score {
            font-size: 24px;
            color: #004411;
            display: flex;
            align-items: center;
            margin: 0 10px;
        }
        .score .icon {
            font-size: 28px;
            margin-right: 5px;
        }
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.5);
        }
        .modal-content {
            background-color: #FFF8DC;
            margin: 15% auto;
            padding: 20px;
            border: 5px solid #004411;
            width: 300px;
            text-align: center;
            border-radius: 10px;
        }
        .modal-content h2 {
            color: #004411;
        }
        .modal-content p {
            font-size: 18px;
            color: #004411;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .modal-content p .icon {
            font-size: 24px;
            margin-right: 5px;
        }
        .restart-button, .start-button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #004411;
            color: #FFD700;
            border: none;
            cursor: pointer;
            margin-top: 20px;
            border-radius: 5px;
        }
        .countdown {
            font-size: 48px;
            color: #004411;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: fadeInOut 1s ease-in-out;
        }
        @keyframes fadeInOut {
            0%, 100% { opacity: 0; }
            50% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="score-container">
        <div class="score" id="player1Score"><span class="icon material-icons" style="color: #004411;">directions_car</span> <span id="score1">0</span></div>
        <div class="score" id="player2Score"><span class="icon material-icons" style="color: #0000FF;">airplane</span> <span id="score2">0</span></div>
    </div>
    <div class="countdown" id="countdown">3</div>
    <div id="gameOverModal" class="modal">
        <div class="modal-content">
            <h2>Game Over</h2>
            <p id="player1FinalScore"><span class="icon material-icons" style="color: #004411;">directions_car</span> Player 1 Score: <span id="finalScore1">0</span></p>
            <p id="player2FinalScore"><span class="icon material-icons" style="color: #0000FF;">airplane</span> Player 2 Score: <span id="finalScore2">0</span></p>
            <p id="winnerText">Winner: None</p>
            <button class="restart-button" id="restartButton">Restart</button>
        </div>
    </div>
    <button class="start-button" id="startButton">Start Game</button>
    <canvas id="gameCanvas" width="400" height="400"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const gameOverModal = document.getElementById('gameOverModal');
        const winnerText = document.getElementById('winnerText');
        const restartButton = document.getElementById('restartButton');
        const startButton = document.getElementById('startButton');
        const countdownDisplay = document.getElementById('countdown');

        const box = 20;
        let snake1 = [{ x: 9 * box, y: 10 * box }];
        let snake2 = [{ x: 10 * box, y: 10 * box }];
        let food = {
            x: Math.floor(Math.random() * 19 + 1) * box,
            y: Math.floor(Math.random() * 19 + 1) * box
        };
        let score1 = 0;
        let score2 = 0;
        let d1 = 'RIGHT';
        let d2 = 'LEFT';
        let game;
        let countdown;

        document.addEventListener('keydown', direction);

        function direction(event) {
            let key = event.keyCode;
            if (key == 37) {
                d1 = 'LEFT';
            } else if (key == 38) {
                d1 = 'UP';
            } else if (key == 39) {
                d1 = 'RIGHT';
            } else if (key == 40) {
                d1 = 'DOWN';
            } else if (key == 65) { // 'A' key
                d2 = 'LEFT';
            } else if (key == 87) { // 'W' key
                d2 = 'UP';
            } else if (key == 68) { // 'D' key
                d2 = 'RIGHT';
            } else if (key == 83) { // 'S' key
                d2 = 'DOWN';
            }
        }

        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            for (let i = 0; i < snake1.length; i++) {
                ctx.fillStyle = i === 0 ? '#004411' : '#4CAF50'; // Snake head and body colors
                ctx.fillRect(snake1[i].x, snake1[i].y, box, box);

                ctx.strokeStyle = '#FFD700';
                ctx.strokeRect(snake1[i].x, snake1[i].y, box, box);
            }

            for (let i = 0; i < snake2.length; i++) {
                ctx.fillStyle = i === 0 ? '#0000FF' : '#ADD8E6'; // Snake head and body colors
                ctx.fillRect(snake2[i].x, snake2[i].y, box, box);

                ctx.strokeStyle = '#FFD700';
                ctx.strokeRect(snake2[i].x, snake2[i].y, box, box);
            }

            ctx.fillStyle = '#FF4500'; // Food color
            ctx.fillRect(food.x, food.y, box, box);

            let snakeX1 = snake1[0].x;
            let snakeY1 = snake1[0].y;
            let snakeX2 = snake2[0].x;
            let snakeY2 = snake2[0].y;

            if (d1 == 'LEFT') snakeX1 -= box;
            if (d1 == 'UP') snakeY1 -= box;
            if (d1 == 'RIGHT') snakeX1 += box;
            if (d1 == 'DOWN') snakeY1 += box;

            if (d2 == 'LEFT') snakeX2 -= box;
            if (d2 == 'UP') snakeY2 -= box;
            if (d2 == 'RIGHT') snakeX2 += box;
            if (d2 == 'DOWN') snakeY2 += box;

            if (snakeX1 == food.x && snakeY1 == food.y) {
                score1++;
                food = {
                    x: Math.floor(Math.random() * 19 + 1) * box,
                    y: Math.floor(Math.random() * 19 + 1) * box
                };
            } else {
                snake1.pop();
            }

            if (snakeX2 == food.x && snakeY2 == food.y) {
                score2++;
                food = {
                    x: Math.floor(Math.random() * 19 + 1) * box,
                    y: Math.floor(Math.random() * 19 + 1) * box
                };
            } else {
                snake2.pop();
            }

            let newHead1 = { x: snakeX1, y: snakeY1 };
            let newHead2 = { x: snakeX2, y: snakeY2 };

            if (snakeX1 < 0 || snakeY1 < 0 || snakeX1 >= canvas.width || snakeY1 >= canvas.height) {
                endGame('<span class="icon material-icons" style="color: #0000FF;">airplane</span>');
            }

            if (snakeX2 < 0 || snakeY2 < 0 || snakeX2 >= canvas.width || snakeY2 >= canvas.height) {
                endGame('<span class="icon material-icons" style="color: #004411;">directions_car</span>');
            }

            snake1.unshift(newHead1);
            snake2.unshift(newHead2);

            document.getElementById('score1').innerText = score1;
            document.getElementById('score2').innerText = score2;
        }

        function endGame(winnerIcon) {
            clearInterval(game);
            document.getElementById('finalScore1').innerText = score1;
            document.getElementById('finalScore2').innerText = score2;
            winnerText.innerHTML = 'Winner: ' + winnerIcon;
            gameOverModal.style.display = 'block';
        }

        function startCountdown() {
            let timeLeft = 3;
            countdownDisplay.innerText = timeLeft;
            countdown = setInterval(() => {
                timeLeft -= 1;
                if (timeLeft >= 0) {
                    countdownDisplay.innerText = timeLeft > 0 ? timeLeft : 'GO!';
                    countdownDisplay.style.animation = 'fadeInOut 1s ease-in-out';
                } else {
                    clearInterval(countdown);
                    countdownDisplay.style.display = 'none';
                    startGame();
                }
            }, 1000);
        }

        function startGame() {
            game = setInterval(draw, 100);
        }

        startButton.addEventListener('click', () => {
            startCountdown();
            startButton.style.display = 'none';
        });

        restartButton.addEventListener('click', () => {
            snake1 = [{ x: 9 * box, y: 10 * box }];
            snake2 = [{ x: 10 * box, y: 10 * box }];
            food = {
                x: Math.floor(Math.random() * 19 + 1) * box,
                y: Math.floor(Math.random() * 19 + 1) * box
            };
            score1 = 0;
            score2 = 0;
            d1 = 'RIGHT';
            d2 = 'LEFT';
            gameOverModal.style.display = 'none';
            countdownDisplay.style.display = 'block';
            startButton.style.display = 'none';
            clearInterval(game);
            clearInterval(countdown);
            startCountdown();
        });
    </script>
</body>
</html>
"""

# Embed the game code in the Streamlit app
components.html(game_code, height=600)
