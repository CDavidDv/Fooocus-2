#!/bin/bash

################################################################################
#
# Script para hacer push a GitHub de Fooocus
# Uso: bash push_to_github.sh
#
################################################################################

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                   PUSH A GITHUB - Fooocus                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 1. Verificar que estamos en un repositorio git
if [ ! -d .git ]; then
    echo "❌ Error: No estamos en un repositorio git"
    echo "   Ejecuta primero: git init"
    exit 1
fi

# 2. Verificar que hay un remote configurado
if ! git remote get-url origin &>/dev/null; then
    echo "❌ Error: No hay un remote 'origin' configurado"
    echo ""
    echo "   Configura el remote con:"
    echo "   git remote add origin https://github.com/tu-usuario/Fooocus.git"
    exit 1
fi

# 3. Mostrar remote actual
REMOTE_URL=$(git remote get-url origin)
echo "📍 Remote configurado: $REMOTE_URL"
echo ""

# 4. Verificar cambios
echo "📋 Estado actual:"
git status --short
echo ""

# 5. Preguntar si continuar
read -p "¿Continuar con el push? (s/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo "❌ Cancelado por el usuario"
    exit 1
fi

# 6. Agregar cambios
echo ""
echo "⏳ Agregando cambios..."
git add .

# 7. Pedir mensaje de commit si hay cambios
if ! git diff-index --quiet HEAD --; then
    echo "✏️  Hay cambios pendientes"
    echo ""
    read -p "Mensaje de commit: " commit_message

    if [ -z "$commit_message" ]; then
        commit_message="update: Cambios generales"
    fi

    echo "📝 Haciendo commit: '$commit_message'"
    git commit -m "$commit_message"
else
    echo "ℹ️  No hay cambios pendientes"
fi

# 8. Hacer push
echo ""
echo "📤 Enviando a GitHub..."
echo ""

CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

git push -u origin $CURRENT_BRANCH

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ¡PUSH COMPLETADO!                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Detalles:"
echo "  • Remote: $REMOTE_URL"
echo "  • Rama: $CURRENT_BRANCH"
echo ""
echo "🔗 Ver en GitHub:"
echo "  $REMOTE_URL/tree/$CURRENT_BRANCH"
echo ""

# 9. Mostrar resumen
echo "📈 Resumen de commits:"
git log --oneline -5
echo ""

echo "✨ ¡Listo!"
